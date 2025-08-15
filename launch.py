#!/usr/bin/env python3
"""
AIMS Object Detection System Launcher
This script launches both the Flask API backend and provides options for the frontend.
"""

import subprocess
import sys
import time
import threading
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask', 'flask-cors', 'torch', 'transformers', 
        'pillow', 'numpy', 'safetensors', 'streamlit'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing_packages)
        print("✅ Dependencies installed!")
    else:
        print("✅ All dependencies are installed!")

def start_flask_server():
    """Start the Flask API server"""
    print("🚀 Starting Flask API Server...")
    try:
        subprocess.run([sys.executable, 'api_server.py'], cwd=Path.cwd())
    except KeyboardInterrupt:
        print("\n🛑 Flask server stopped.")
    except Exception as e:
        print(f"❌ Error starting Flask server: {e}")

def start_streamlit_app():
    """Start the Streamlit app"""
    print("🚀 Starting Streamlit App...")
    try:
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'], cwd=Path.cwd())
    except KeyboardInterrupt:
        print("\n🛑 Streamlit app stopped.")
    except Exception as e:
        print(f"❌ Error starting Streamlit app: {e}")

def open_browser_after_delay(url, delay=3):
    """Open browser after a delay"""
    time.sleep(delay)
    webbrowser.open(url)

def main():
    print("="*60)
    print("🎯 AIMS Object Detection System Launcher")
    print("="*60)
    
    # Check dependencies
    check_dependencies()
    
    print("\nChoose launch option:")
    print("1. Flask API Server only (Web Interface)")
    print("2. Streamlit App only (Interactive UI)")
    print("3. Both Flask API + Streamlit (Recommended)")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        print("\n🌐 Starting Flask API Server...")
        print("📍 Web Interface: http://localhost:5000")
        print("📍 API Endpoint: http://localhost:5000/api/detect")
        
        # Open browser after delay
        threading.Thread(target=open_browser_after_delay, args=("http://localhost:5000",), daemon=True).start()
        start_flask_server()
        
    elif choice == '2':
        print("\n🎨 Starting Streamlit App...")
        print("📍 Streamlit Interface: http://localhost:8501")
        start_streamlit_app()
        
    elif choice == '3':
        print("\n🚀 Starting both Flask API and Streamlit App...")
        print("📍 Flask Web Interface: http://localhost:5000")
        print("📍 Streamlit Interface: http://localhost:8501")
        print("📍 API Endpoint: http://localhost:5000/api/detect")
        
        # Start Flask server in a separate thread
        flask_thread = threading.Thread(target=start_flask_server, daemon=True)
        flask_thread.start()
        
        # Wait a bit for Flask to start
        time.sleep(2)
        
        # Open browsers
        threading.Thread(target=open_browser_after_delay, args=("http://localhost:5000",), daemon=True).start()
        threading.Thread(target=open_browser_after_delay, args=("http://localhost:8501", 5), daemon=True).start()
        
        # Start Streamlit (this will block)
        start_streamlit_app()
        
    elif choice == '4':
        print("👋 Goodbye!")
        sys.exit(0)
        
    else:
        print("❌ Invalid choice. Please try again.")
        main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
