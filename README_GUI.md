# AIMS Object Detection GUI

## Overview
A modern web-based GUI for the AIMS (Advanced Intelligent Monitoring System) object detection project by Sarthak. This system provides a sleek black and white interface for real-time object detection using the OwlViT model.

## Features
- **Modern Landing Page**: Dynamic black and white design with AIMS branding
- **Real-time Object Detection**: Upload images and detect objects using natural language queries
- **API Integration**: Flask backend with RESTful API endpoints
- **Responsive Design**: Works on desktop and mobile devices
- **Visual Results**: Displays detection results with bounding boxes and confidence scores

## System Components

### 1. Web Interface (`index.html`)
- Modern landing page with AIMS logo and branding
- File upload for images
- Text input for detection queries
- Real-time results display with visual feedback
- Animated particles and dynamic effects

### 2. API Server (`api_server.py`)
- Flask-based REST API
- OwlViT model integration
- Image processing and object detection
- CORS enabled for web interface
- Health check endpoints

### 3. Model Files
- Pre-trained OwlViT model (`model.safetensors`)
- Configuration files (`config.json`, `preprocessor_config.json`)
- Tokenizer files for text processing

## Quick Start

### Prerequisites
```bash
pip install flask flask-cors torch transformers pillow numpy
```

### Running the System

1. **Start the API Server**:
   ```bash
   python api_server.py
   ```
   The server will start on `http://localhost:5000`

2. **Access the Web Interface**:
   Open your browser and go to `http://localhost:5000`

### Usage

1. **Upload an Image**: Click "Choose File" and select an image
2. **Enter Detection Query**: Type what you want to detect (e.g., "license plate", "person", "car")
3. **Start Detection**: Click the "Start Detection" button
4. **View Results**: See the detection results with bounding boxes and confidence scores

## API Endpoints

### POST `/api/detect`
Perform object detection on an uploaded image.

**Parameters**:
- `image`: Image file (multipart/form-data)
- `query`: Detection query string
- `confidence_threshold`: Minimum confidence (optional, default: 0.1)
- `detection_mode`: "single" or "multiple" (optional, default: "multiple")
- `nms_threshold`: NMS threshold (optional, default: 0.5)

**Response**:
```json
{
  "success": true,
  "query": "license plate",
  "detections": [
    {
      "box": [x1, y1, x2, y2],
      "score": 0.85,
      "label": 0,
      "query": "license plate"
    }
  ],
  "detection_count": 1,
  "image_data": "data:image/png;base64,...",
  "parameters": {
    "confidence_threshold": 0.1,
    "detection_mode": "multiple",
    "nms_threshold": 0.5
  }
}
```

### GET `/api/health`
Check API server health and model status.

**Response**:
```json
{
  "status": "healthy",
  "model_status": "loaded",
  "timestamp": "2024-08-14T17:44:00.123456"
}
```

## Design Features

### Visual Design
- **Color Scheme**: Black and white with gradient backgrounds
- **Typography**: Clean, modern fonts with proper hierarchy
- **Animations**: Smooth transitions, floating particles, pulse effects
- **Responsive**: Mobile-friendly design with adaptive layouts

### User Experience
- **Loading States**: Visual feedback during processing
- **Error Handling**: Clear error messages and troubleshooting tips
- **Real-time Updates**: Live status updates and progress indicators
- **Accessibility**: Keyboard navigation and screen reader support

## Technical Architecture

```
┌─────────────────┐    HTTP/API    ┌─────────────────┐
│   Web Browser   │ ──────────────► │  Flask Server   │
│   (index.html)  │                 │ (api_server.py) │
└─────────────────┘                 └─────────────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │   OwlViT Model  │
                                    │ (model files)   │
                                    └─────────────────┘
```

## Troubleshooting

### Common Issues

1. **Model Loading Errors**:
   - Ensure all model files are present in the directory
   - Check transformers library version compatibility

2. **API Connection Errors**:
   - Verify Flask server is running on port 5000
   - Check firewall settings
   - Ensure CORS is properly configured

3. **Detection Issues**:
   - Try different query phrases
   - Adjust confidence threshold
   - Use higher quality images

### Server Logs
Monitor the Flask server terminal for detailed error messages and request logs.

## Development

### File Structure
```
Aims_v3/
├── index.html              # Web interface
├── api_server.py          # Flask API server
├── app.py                 # Original Streamlit app
├── model.safetensors      # Model weights
├── config.json            # Model configuration
├── preprocessor_config.json
├── tokenizer files...
└── README_GUI.md          # This file
```

### Customization
- Modify `index.html` for UI changes
- Update `api_server.py` for backend functionality
- Adjust model parameters in detection functions

## Credits
- **Project**: AIMS Society Object Detection System
- **Developer**: Sarthak
- **Model**: OwlViT (Open-vocabulary Object Detection)
- **Framework**: Flask + HTML/CSS/JavaScript