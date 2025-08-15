# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for model files
RUN mkdir -p /app/models

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=api_server.py
ENV FLASK_ENV=production
ENV MODEL_CACHE_DIR=/app/models

# Expose ports
EXPOSE 5000 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Create a non-root user
RUN useradd -m -u 1000 aimsuser && \
    chown -R aimsuser:aimsuser /app
USER aimsuser

# Default command (can be overridden)
CMD ["python", "api_server.py"]

# Alternative commands:
# For Streamlit: CMD ["python", "app.py"]
# For auto-launcher: CMD ["python", "launch.py"]

# Build instructions:
# docker build -t aims-vision .
# docker run -p 5000:5000 -p 8501:8501 aims-vision

# For GPU support, use nvidia/cuda base image:
# FROM nvidia/cuda:11.8-runtime-ubuntu20.04
# Then install Python and dependencies