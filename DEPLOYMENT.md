# 🚀 AIMS Vision System - Deployment Guide

This guide covers various deployment options for the AIMS Vision System, from local development to production cloud deployments.

## 📋 Prerequisites

- Docker and Docker Compose (recommended)
- Python 3.8+ (for local deployment)
- Git for version control
- At least 4GB RAM, 8GB recommended
- GPU support (optional, for faster inference)

## 🏠 Local Development

### Option 1: Direct Python Execution

```bash
# Clone the repository
git clone https://github.com/yourusername/aims-vision-system.git
cd aims-vision-system

# Install dependencies
pip install -r requirements.txt

# Download model files (see README for details)
# Place model files in the project directory

# Run the application
python launch.py  # Auto-launcher
# OR
python api_server.py  # API only
# OR
python app.py  # Streamlit only
```

### Option 2: Docker Development

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## ☁️ Cloud Deployment Options

### 1. AWS Deployment

#### AWS ECS (Elastic Container Service)

```bash
# Build and push to ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-west-2.amazonaws.com

docker build -t aims-vision .
docker tag aims-vision:latest <account-id>.dkr.ecr.us-west-2.amazonaws.com/aims-vision:latest
docker push <account-id>.dkr.ecr.us-west-2.amazonaws.com/aims-vision:latest

# Create ECS task definition and service
# Use the provided ecs-task-definition.json
```

#### AWS Lambda (for API only)

```bash
# Install AWS SAM CLI
pip install aws-sam-cli

# Deploy with SAM
sam build
sam deploy --guided
```

#### AWS EC2

```bash
# Launch EC2 instance with Docker
# SSH into instance
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone and run
git clone https://github.com/yourusername/aims-vision-system.git
cd aims-vision-system
docker-compose up -d
```

### 2. Google Cloud Platform

#### Cloud Run

```bash
# Build and deploy to Cloud Run
gcloud builds submit --tag gcr.io/PROJECT-ID/aims-vision
gcloud run deploy --image gcr.io/PROJECT-ID/aims-vision --platform managed
```

#### Google Kubernetes Engine (GKE)

```bash
# Create GKE cluster
gcloud container clusters create aims-cluster --num-nodes=3

# Deploy with Kubernetes
kubectl apply -f k8s/
```

#### Compute Engine

```bash
# Create VM instance
gcloud compute instances create aims-vm \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --machine-type=n1-standard-2 \
  --boot-disk-size=20GB

# SSH and setup
gcloud compute ssh aims-vm
# Follow EC2 setup steps
```

### 3. Microsoft Azure

#### Azure Container Instances

```bash
# Create resource group
az group create --name aims-rg --location eastus

# Deploy container
az container create \
  --resource-group aims-rg \
  --name aims-container \
  --image yourusername/aims-vision:latest \
  --ports 5000 8501 \
  --memory 4 \
  --cpu 2
```

#### Azure Kubernetes Service (AKS)

```bash
# Create AKS cluster
az aks create \
  --resource-group aims-rg \
  --name aims-aks \
  --node-count 3 \
  --enable-addons monitoring \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group aims-rg --name aims-aks

# Deploy
kubectl apply -f k8s/
```

### 4. DigitalOcean

#### App Platform

```yaml
# app.yaml
name: aims-vision-system
services:
- name: api
  source_dir: /
  github:
    repo: yourusername/aims-vision-system
    branch: main
  run_command: python api_server.py
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  http_port: 5000
  routes:
  - path: /api
```

#### Droplets

```bash
# Create droplet with Docker
# SSH into droplet
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Clone and run
git clone https://github.com/yourusername/aims-vision-system.git
cd aims-vision-system
docker-compose up -d
```

### 5. Heroku

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create aims-vision-app

# Set buildpack
heroku buildpacks:set heroku/python

# Configure environment variables
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main
```

## 🔧 Production Configuration

### Environment Variables

```bash
# Required
FLASK_ENV=production
MODEL_CACHE_DIR=/app/models

# Optional
REDIS_URL=redis://localhost:6379
DATABASE_URL=postgresql://user:pass@localhost/aims
SECRET_KEY=your-secret-key
MAX_UPLOAD_SIZE=50MB
API_RATE_LIMIT=100/hour
```

### SSL/TLS Configuration

```nginx
# nginx-ssl.conf
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=63072000" always;
    
    # Your location blocks here
}
```

### Database Setup (Optional)

```sql
-- PostgreSQL schema for storing detection results
CREATE TABLE detections (
    id SERIAL PRIMARY KEY,
    image_hash VARCHAR(64) NOT NULL,
    query TEXT NOT NULL,
    results JSONB NOT NULL,
    confidence FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_detections_hash ON detections(image_hash);
CREATE INDEX idx_detections_created ON detections(created_at);
```

## 📊 Monitoring and Logging

### Health Checks

```bash
# API health check
curl -f http://localhost:5000/api/health

# Streamlit health check
curl -f http://localhost:8501/healthz
```

### Logging Configuration

```python
# logging_config.py
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        RotatingFileHandler('aims.log', maxBytes=10485760, backupCount=5),
        logging.StreamHandler()
    ]
)
```

### Prometheus Metrics

```python
# metrics.py
from prometheus_client import Counter, Histogram, generate_latest

DETECTION_REQUESTS = Counter('detection_requests_total', 'Total detection requests')
DETECTION_DURATION = Histogram('detection_duration_seconds', 'Detection processing time')
```

## 🔒 Security Considerations

### API Security

```python
# Add to api_server.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/detect', methods=['POST'])
@limiter.limit("10 per minute")
def detect():
    # Your detection logic
    pass
```

### Input Validation

```python
# validation.py
from PIL import Image
import magic

def validate_image(file_data):
    # Check file type
    file_type = magic.from_buffer(file_data, mime=True)
    if file_type not in ['image/jpeg', 'image/png', 'image/webp']:
        raise ValueError("Invalid file type")
    
    # Check image size
    try:
        img = Image.open(io.BytesIO(file_data))
        if img.size[0] > 4096 or img.size[1] > 4096:
            raise ValueError("Image too large")
    except Exception:
        raise ValueError("Invalid image file")
```

## 🚨 Troubleshooting

### Common Issues

1. **Out of Memory**
   ```bash
   # Increase Docker memory limit
   docker run -m 8g aims-vision
   ```

2. **Model Loading Errors**
   ```bash
   # Check model files
   ls -la *.safetensors *.pth
   # Verify file integrity
   sha256sum model.safetensors
   ```

3. **Port Conflicts**
   ```bash
   # Check port usage
   netstat -tulpn | grep :5000
   # Use different ports
   docker-compose -f docker-compose.override.yml up
   ```

### Performance Optimization

```python
# optimization.py
import torch

# Enable optimizations
torch.backends.cudnn.benchmark = True
torch.backends.cudnn.deterministic = False

# Use mixed precision
from torch.cuda.amp import autocast

@autocast()
def detect_objects(image, queries):
    # Your detection logic with automatic mixed precision
    pass
```

## 📈 Scaling

### Horizontal Scaling

```yaml
# docker-compose.scale.yml
version: '3.8'
services:
  aims-api:
    deploy:
      replicas: 3
  nginx:
    depends_on:
      - aims-api
```

### Load Balancing

```nginx
# nginx-lb.conf
upstream aims_backend {
    least_conn;
    server aims-api-1:5000;
    server aims-api-2:5000;
    server aims-api-3:5000;
}
```

## 🎯 Best Practices

1. **Use environment-specific configurations**
2. **Implement proper logging and monitoring**
3. **Set up automated backups for persistent data**
4. **Use secrets management for sensitive data**
5. **Implement CI/CD pipelines for automated deployments**
6. **Regular security updates and vulnerability scanning**
7. **Performance monitoring and optimization**
8. **Disaster recovery planning**

---

For more detailed deployment instructions for specific platforms, please refer to the respective cloud provider documentation or create an issue in the repository.