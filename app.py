import streamlit as st
import torch
from transformers.models.owlvit import OwlViTProcessor, OwlViTForObjectDetection
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io

# Set page config
st.set_page_config(
    page_title="OwlViT Object Detection",
    page_icon="🦉",
    layout="wide"
)

# Cache the model loading
@st.cache_resource
def load_model():
    """Load the OwlViT model and processor"""
    try:
        processor = OwlViTProcessor.from_pretrained(".")
        model = OwlViTForObjectDetection.from_pretrained(".")
        return processor, model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None

def calculate_iou(box1, box2):
    """Calculate Intersection over Union (IoU) of two bounding boxes"""
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2
    
    # Calculate intersection area
    inter_x_min = max(x1_min, x2_min)
    inter_y_min = max(y1_min, y2_min)
    inter_x_max = min(x1_max, x2_max)
    inter_y_max = min(y1_max, y2_max)
    
    if inter_x_max <= inter_x_min or inter_y_max <= inter_y_min:
        return 0.0
    
    inter_area = (inter_x_max - inter_x_min) * (inter_y_max - inter_y_min)
    
    # Calculate union area
    box1_area = (x1_max - x1_min) * (y1_max - y1_min)
    box2_area = (x2_max - x2_min) * (y2_max - y2_min)
    union_area = box1_area + box2_area - inter_area
    
    return inter_area / union_area if union_area > 0 else 0.0

def apply_nms(boxes, scores, iou_threshold=0.5):
    """Apply Non-Maximum Suppression to remove overlapping detections"""
    if len(boxes) == 0:
        return np.array([], dtype=int)
    
    # If only one detection, return it
    if len(boxes) == 1:
        return np.array([0])
    
    # Sort by confidence scores in descending order
    sorted_indices = np.argsort(scores)[::-1]
    
    keep = []
    suppressed = set()
    
    for i in range(len(sorted_indices)):
        current_idx = sorted_indices[i]
        
        # Skip if already suppressed
        if current_idx in suppressed:
            continue
            
        # Keep this detection
        keep.append(current_idx)
        
        # Suppress overlapping detections
        for j in range(i + 1, len(sorted_indices)):
            other_idx = sorted_indices[j]
            
            if other_idx in suppressed:
                continue
                
            iou = calculate_iou(boxes[current_idx], boxes[other_idx])
            if iou >= iou_threshold:
                suppressed.add(other_idx)
    
    return np.array(keep)

def draw_bounding_boxes(image, boxes, scores, labels, threshold=0.1):
    """Draw bounding boxes on the image"""
    draw = ImageDraw.Draw(image)
    
    # Try to load a font, fallback to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown']
    
    for i, (box, score, label) in enumerate(zip(boxes, scores, labels)):
        if score > threshold:
            color = colors[i % len(colors)]
            
            # Convert normalized coordinates to pixel coordinates
            x1, y1, x2, y2 = box
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # Draw bounding box
            draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
            
            # Draw label and score
            text = f"{label}: {score:.2f}"
            bbox = draw.textbbox((x1, y1), text, font=font)
            draw.rectangle(bbox, fill=color)
            draw.text((x1, y1), text, fill='white', font=font)
    
    return image

def main():
    st.title("🦉 OwlViT Object Detection")
    st.markdown("Upload an image and enter a text query to detect objects!")
    
    # Load model
    processor, model = load_model()
    
    if processor is None or model is None:
        st.error("Failed to load the model. Please check if all model files are present.")
        return
    
    # Create two columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("Input")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=["jpg", "jpeg", "png", "bmp", "tiff"]
        )
        
        # Text query input
        query = st.text_input(
            "Enter your query (e.g., 'a cat', 'person', 'car'):",
            placeholder="What object do you want to detect?"
        )
        
        # Detection threshold
        threshold = st.slider(
            "Detection Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.05,
            help="Minimum confidence score for detections"
        )
        
        # Detection mode
        detection_mode = st.selectbox(
            "Detection Mode",
            ["Best Single Detection", "Multiple Detections with NMS"],
            help="Choose whether to show only the best detection or multiple filtered detections"
        )
        
        # IoU threshold for NMS (only show if multiple detections mode)
        if detection_mode == "Multiple Detections with NMS":
            iou_threshold = st.slider(
                "NMS IoU Threshold",
                min_value=0.1,
                max_value=0.9,
                value=0.5,
                step=0.1,
                help="Higher values = more aggressive filtering of overlapping detections"
            )
        else:
            iou_threshold = 0.5  # Default value, won't be used
        
        # Detect button
        detect_button = st.button("🔍 Detect Objects", type="primary")
    
    with col2:
        st.header("Results")
        
        if uploaded_file is not None:
            # Display original image
            image = Image.open(uploaded_file).convert("RGB")
            st.subheader("Original Image")
            st.image(image, use_column_width=True)
            
            if detect_button and query.strip():
                with st.spinner("Detecting objects..."):
                    try:
                        # Prepare inputs
                        text_queries = [query.strip()]
                        inputs = processor(text=text_queries, images=image, return_tensors="pt")
                        
                        # Run inference
                        with torch.no_grad():
                            outputs = model(**inputs)
                        
                        # Post-process results
                        target_sizes = torch.Tensor([image.size[::-1]])
                        results = processor.post_process_object_detection(
                            outputs=outputs, 
                            target_sizes=target_sizes, 
                            threshold=threshold
                        )
                        
                        # Get results for the first (and only) image
                        boxes = results[0]["boxes"].cpu().numpy()
                        scores = results[0]["scores"].cpu().numpy()
                        labels = results[0]["labels"].cpu().numpy()
                        
                        # Apply detection filtering based on selected mode
                        if len(boxes) > 0:
                            if detection_mode == "Best Single Detection":
                                # Keep only the highest confidence detection
                                best_idx = np.argmax(scores)
                                boxes = boxes[best_idx:best_idx+1]
                                scores = scores[best_idx:best_idx+1]
                                labels = labels[best_idx:best_idx+1]
                            else:
                                # Apply Non-Maximum Suppression for multiple detections
                                keep_indices = apply_nms(boxes, scores, iou_threshold=iou_threshold)
                                boxes = boxes[keep_indices]
                                scores = scores[keep_indices]
                                labels = labels[keep_indices]
                        
                        if len(boxes) > 0:
                            # Create a copy of the image for drawing
                            result_image = image.copy()
                            
                            # Draw bounding boxes
                            label_names = [query.strip()] * len(boxes)
                            result_image = draw_bounding_boxes(
                                result_image, boxes, scores, label_names, threshold
                            )
                            
                            # Display results
                            st.subheader("Detection Results")
                            st.image(result_image, use_column_width=True)
                            
                            # Display detection details
                            st.subheader("Detection Details")
                            for i, (box, score) in enumerate(zip(boxes, scores)):
                                if score > threshold:
                                    x1, y1, x2, y2 = box
                                    st.write(f"**Detection {i+1}:**")
                                    st.write(f"- Object: {query.strip()}")
                                    st.write(f"- Confidence: {score:.3f}")
                                    st.write(f"- Bounding Box: ({x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f})")
                                    st.write("---")
                        else:
                            st.warning(f"No objects matching '{query}' were detected with confidence > {threshold}. Try lowering the threshold or using a different query.")
                    
                    except Exception as e:
                        st.error(f"Error during detection: {str(e)}")
            
            elif detect_button and not query.strip():
                st.warning("Please enter a query to detect objects.")
        
        else:
            st.info("Please upload an image to get started.")
    
    # Add some information in the sidebar
    with st.sidebar:
        st.header("About")
        st.write("""
        This app uses the **OwlViT** (Owl Vision Transformer) model for object detection.
        
        **How to use:**
        1. Upload an image
        2. Enter a text description of what you want to detect
        3. Choose detection mode (single best vs multiple)
        4. Adjust the detection threshold if needed
        5. If using multiple detections, adjust NMS threshold
        6. Click 'Detect Objects'
        
        **Detection Modes:**
        - **Best Single Detection**: Shows only the highest confidence match (recommended for single objects)
        - **Multiple Detections with NMS**: Shows multiple filtered detections (for finding all instances)
        
        **Tips:**
        - Use simple, clear descriptions (e.g., "cat", "person", "car")
        - **Detection Threshold**: Lower = more detections, Higher = fewer but more confident
        - For single object queries (like "license plate"), use "Best Single Detection"
        - For multiple objects (like "person"), use "Multiple Detections with NMS"
        - The model works best with common objects and clear images
        """)
        
        st.header("Model Info")
        st.write("""
        - **Model**: OwlViT for Object Detection
        - **Input Size**: 768x768 pixels
        - **Text Encoder**: 12 layers, 8 attention heads
        - **Vision Encoder**: 12 layers, 12 attention heads
        """)

if __name__ == "__main__":
    main()