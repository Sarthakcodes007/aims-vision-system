from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import torch
from transformers.models.owlvit import OwlViTProcessor, OwlViTForObjectDetection
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io
import base64
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables for model and processor
processor = None
model = None

def load_model():
    """Load the OwlViT model and processor"""
    global processor, model
    try:
        processor = OwlViTProcessor.from_pretrained(".")
        model = OwlViTForObjectDetection.from_pretrained(".")
        print("Model loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def non_max_suppression_improved(boxes, scores, iou_threshold=0.5):
    """Improved Non-Maximum Suppression with better handling of edge cases"""
    if len(boxes) == 0:
        return []
    
    # Convert to numpy arrays
    boxes = np.array(boxes)
    scores = np.array(scores)
    
    # Sort by scores in descending order
    indices = np.argsort(scores)[::-1]
    
    keep = []
    while len(indices) > 0:
        # Pick the box with highest score
        current = indices[0]
        keep.append(current)
        
        if len(indices) == 1:
            break
            
        # Calculate IoU with remaining boxes
        current_box = boxes[current]
        remaining_boxes = boxes[indices[1:]]
        
        # Calculate intersection areas
        x1 = np.maximum(current_box[0], remaining_boxes[:, 0])
        y1 = np.maximum(current_box[1], remaining_boxes[:, 1])
        x2 = np.minimum(current_box[2], remaining_boxes[:, 2])
        y2 = np.minimum(current_box[3], remaining_boxes[:, 3])
        
        # Calculate intersection area
        intersection_area = np.maximum(0, x2 - x1) * np.maximum(0, y2 - y1)
        
        # Calculate union area
        current_area = (current_box[2] - current_box[0]) * (current_box[3] - current_box[1])
        remaining_areas = (remaining_boxes[:, 2] - remaining_boxes[:, 0]) * (remaining_boxes[:, 3] - remaining_boxes[:, 1])
        union_area = current_area + remaining_areas - intersection_area
        
        # Calculate IoU
        iou = intersection_area / (union_area + 1e-6)  # Add small epsilon to avoid division by zero
        
        # Keep boxes with IoU less than threshold
        indices = indices[1:][iou < iou_threshold]
    
    return keep

def detect_objects(image, text_queries, confidence_threshold=0.1, detection_mode="multiple", nms_threshold=0.5):
    """Detect objects in image using OwlViT model"""
    try:
        # Process inputs
        inputs = processor(text=text_queries, images=image, return_tensors="pt")
        
        # Get predictions
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Post-process predictions with very low threshold to get all detections
        target_sizes = torch.Tensor([image.size[::-1]])
        results = processor.post_process_object_detection(
            outputs=outputs, 
            target_sizes=target_sizes, 
            threshold=0.01  # Use very low threshold to capture all possible detections
        )
        
        detections = []
        
        for result in results:
            boxes = result["boxes"].cpu().numpy()
            scores = result["scores"].cpu().numpy()
            labels = result["labels"].cpu().numpy()
            
            if len(boxes) > 0:
                # Apply detection mode logic
                if detection_mode == "single":
                    # Always get the highest confidence detection (ignore confidence threshold)
                    best_idx = np.argmax(scores)
                    keep_indices = [best_idx]
                else:
                    # For multiple detections, filter by confidence threshold then apply NMS
                    valid_indices = np.where(scores >= confidence_threshold)[0]
                    if len(valid_indices) == 0:
                        # If no detections meet threshold, still show the best one
                        valid_indices = [np.argmax(scores)]
                    
                    valid_boxes = boxes[valid_indices]
                    valid_scores = scores[valid_indices]
                    nms_indices = non_max_suppression_improved(valid_boxes, valid_scores, nms_threshold)
                    keep_indices = [valid_indices[i] for i in nms_indices]
                
                # Collect kept detections
                for idx in keep_indices:
                    detections.append({
                        "box": boxes[idx].tolist(),
                        "score": float(scores[idx]),
                        "label": int(labels[idx]),
                        "query": text_queries[labels[idx]] if labels[idx] < len(text_queries) else "unknown"
                    })
        
        return detections
    
    except Exception as e:
        print(f"Detection error: {e}")
        return []

def draw_detections(image, detections):
    """Draw bounding boxes on image"""
    draw = ImageDraw.Draw(image)
    
    # Try to load a font, fallback to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
    
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'cyan', 'magenta']
    
    for i, detection in enumerate(detections):
        box = detection['box']
        score = detection['score']
        query = detection['query']
        
        color = colors[i % len(colors)]
        
        # Draw bounding box
        draw.rectangle(box, outline=color, width=3)
        
        # Draw label
        label = f"{query}: {score:.2f}"
        
        # Get text bounding box for background
        bbox = draw.textbbox((box[0], box[1] - 25), label, font=font)
        draw.rectangle(bbox, fill=color)
        draw.text((box[0], box[1] - 25), label, fill='white', font=font)
    
    return image

@app.route('/api/detect', methods=['POST'])
def api_detect():
    """API endpoint for object detection"""
    try:
        # Check if model is loaded
        if processor is None or model is None:
            return jsonify({"error": "Model not loaded. Please restart the server."}), 500
        
        # Get image and query from request
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        if 'query' not in request.form:
            return jsonify({"error": "No query provided"}), 400
        
        image_file = request.files['image']
        query = request.form['query'].strip()
        
        if not query:
            return jsonify({"error": "Query cannot be empty"}), 400
        
        # Load and process image
        image = Image.open(image_file.stream).convert('RGB')
        
        # Get optional parameters
        confidence_threshold = float(request.form.get('confidence_threshold', 0.1))
        detection_mode = request.form.get('detection_mode', 'single')
        nms_threshold = float(request.form.get('nms_threshold', 0.5))
        
        # Perform detection
        text_queries = [query]
        detections = detect_objects(
            image, 
            text_queries, 
            confidence_threshold=confidence_threshold,
            detection_mode=detection_mode,
            nms_threshold=nms_threshold
        )
        
        # Draw detections on image
        result_image = image.copy()
        if detections:
            result_image = draw_detections(result_image, detections)
        
        # Convert image to base64 for response
        img_buffer = io.BytesIO()
        result_image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        
        return jsonify({
            "success": True,
            "query": query,
            "detections": detections,
            "detection_count": len(detections),
            "image_data": f"data:image/png;base64,{img_base64}",
            "parameters": {
                "confidence_threshold": confidence_threshold,
                "detection_mode": detection_mode,
                "nms_threshold": nms_threshold
            }
        })
    
    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({"error": f"Detection failed: {str(e)}"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    model_status = "loaded" if (processor is not None and model is not None) else "not_loaded"
    return jsonify({
        "status": "healthy",
        "model_status": model_status,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/', methods=['GET'])
def serve_index():
    """Serve the main HTML page"""
    return send_file('index.html')

@app.route('/detection.html', methods=['GET'])
def serve_detection():
    """Serve the detection page"""
    return send_file('detection.html')

@app.route('/aims_logo.svg', methods=['GET'])
def serve_logo():
    """Serve the AIMS DTU logo"""
    return send_file('aims_logo.svg', mimetype='image/svg+xml')

if __name__ == '__main__':
    print("Starting AIMS Object Detection API Server...")
    
    # Load model on startup
    if load_model():
        print("Model loaded successfully!")
        print("Starting Flask server on http://localhost:5000")
        print("API endpoint: http://localhost:5000/api/detect")
        print("Web interface: http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("Failed to load model. Please check your model files.")