# AIMS - Advanced AI Vision System

🚀 **A cutting-edge object detection system powered by OwlViT (Owl Vision Transformer) with an immersive 3D web interface**

This project combines state-of-the-art computer vision with modern web technologies to create an interactive object detection experience featuring advanced 3D visualizations, parallax effects, and real-time AI inference.

## ✨ Features

### 🤖 AI-Powered Detection
- **Zero-Shot Object Detection**: Detect any object using natural language descriptions
- **OwlViT Architecture**: Transformer-based vision-language model
- **Real-Time Processing**: Fast inference with optimized pipeline
- **High Accuracy**: State-of-the-art detection performance

### 🎨 Advanced 3D Interface
- **Immersive Landing Page**: Dynamic 3D animations with Three.js
- **Parallax Scrolling**: Multi-layer depth effects with smooth transitions
- **Particle Systems**: Interactive particle animations with mouse tracking
- **Level of Detail (LOD)**: Performance-optimized 3D rendering
- **Atmospheric Effects**: Realistic fog and lighting systems

### 🌐 Modern Web Stack
- **Responsive Design**: Works seamlessly on desktop and mobile
- **RESTful API**: Flask backend with CORS support
- **Real-Time Results**: WebSocket integration for live updates
- **Glassmorphism UI**: Modern design with smooth animations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- 4GB+ RAM recommended
- Modern web browser with WebGL support

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/aims-vision-system.git
   cd aims-vision-system
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download Model Files** (⚠️ **Important**):
   Due to GitHub's file size limitations, you need to download the pre-trained model files:
   - Download OwlViT model files from [Hugging Face](https://huggingface.co/google/owlvit-base-patch32)
   - Place the following files in the project root:
     - `model.safetensors` (~1.4GB)
     - `checkpoint.pth`
     - All configuration files are included in the repository

### Usage

#### Option 1: Web Interface (Recommended)
```bash
python api_server.py
```
Then open `http://localhost:5000` in your browser

#### Option 2: Streamlit Interface
```bash
streamlit run app.py
```
Open `http://localhost:8501`

#### Option 3: Auto-Launch
```bash
python launch.py
```
Automatically starts the server and opens your browser

## Example Queries

- `"a cat"` - Detect cats in the image
- `"person"` - Detect people
- `"red car"` - Detect red cars
- `"dog playing"` - Detect dogs that appear to be playing
- `"book on table"` - Detect books on tables

## Tips for Best Results

- Use clear, simple descriptions
- Try different threshold values (0.05-0.3 typically work well)
- The model works best with common objects and clear images
- If you get too many false positives, increase the threshold
- If you miss detections, decrease the threshold

## 🏗️ Technical Architecture

### Model Architecture
- **Base Model**: OwlViT (Owl Vision Transformer)
- **Framework**: PyTorch + Hugging Face Transformers
- **Vision Encoder**: 12-layer ViT with 768 hidden dimensions
- **Text Encoder**: 12-layer transformer with 512 hidden dimensions
- **Input Resolution**: 768×768 pixels
- **Zero-Shot Capability**: No retraining required for new object classes

### Backend Stack
- **API Framework**: Flask with CORS support
- **Deep Learning**: PyTorch 2.0+ with TorchVision
- **Image Processing**: Pillow (PIL) for image manipulation
- **Model Format**: SafeTensors for secure model loading

### Frontend Stack
- **3D Graphics**: Three.js r128 for WebGL rendering
- **UI Framework**: Vanilla HTML5/CSS3/JavaScript
- **Design System**: Custom glassmorphism with CSS animations
- **Performance**: LOD system and particle culling for optimization

## 🎯 Usage Examples

### Detection Queries
- `"a cat"` - Detect cats in the image
- `"person wearing red shirt"` - Detect people with specific clothing
- `"car in parking lot"` - Detect vehicles in specific contexts
- `"dog playing with ball"` - Detect objects with actions
- `"book on wooden table"` - Detect objects with spatial relationships

### API Usage
```python
import requests
import base64

# Encode image to base64
with open('image.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode()

# Make detection request
response = requests.post('http://localhost:5000/api/detect', json={
    'image': image_data,
    'queries': ['cat', 'dog', 'person'],
    'threshold': 0.1
})

results = response.json()
```

## 🛠️ Development

### Project Structure
```
aims-vision-system/
├── api_server.py          # Flask API backend
├── app.py                 # Streamlit interface
├── launch.py              # Multi-mode launcher
├── index.html             # Main landing page
├── detection.html         # Detection interface
├── requirements.txt       # Python dependencies
├── config.json           # Model configuration
├── preprocessor_config.json # Image preprocessing
├── tokenizer_config.json  # Text tokenization
└── README.md             # This file
```

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

- **Model Loading Error**: Ensure model files are downloaded and placed correctly
- **Memory Issues**: Reduce image size or close other applications
- **No Detections**: Try lowering the threshold (0.05-0.15)
- **Too Many False Positives**: Increase threshold (0.2-0.4)
- **3D Performance Issues**: Disable hardware acceleration or use a different browser

## 📋 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **GPU**: CUDA-compatible (optional, for faster inference)
- **Browser**: Chrome, Firefox, Safari, or Edge with WebGL support
- **Storage**: 2GB free space for model files

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Google Research](https://github.com/google-research/scenic) for the OwlViT model
- [Hugging Face](https://huggingface.co/) for the transformers library
- [Three.js](https://threejs.org/) for 3D graphics capabilities
- The open-source community for inspiration and support

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/yourusername/aims-vision-system/issues) page
2. Create a new issue with detailed information
3. Join our community discussions

---

⭐ **Star this repository if you find it useful!** ⭐