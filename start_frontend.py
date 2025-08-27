#!/usr/bin/env python3
"""
Startup script for Asset Data Privacy Web Frontend
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = ['flask', 'openai', 'PyPDF2']
    missing_packages = []
    
    # Check PyMuPDF separately since it's imported as 'fitz'
    try:
        import fitz
    except ImportError:
        missing_packages.append('PyMuPDF')
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nPlease install missing packages with:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def check_openai_key():
    """Check if OpenAI API key is set."""
    if not os.environ.get('OPENAI_API_KEY'):
        print("⚠️  Warning: OpenAI API key not set")
        print("   Set the OPENAI_API_KEY environment variable to enable AI analysis")
        print("   Example: export OPENAI_API_KEY='your-api-key-here'")
        print()
    else:
        print("✅ OpenAI API key is configured")
    
    return True

def create_directories():
    """Create necessary directories."""
    directories = ['uploads', 'output', 'templates', 'static/css', 'static/js']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Directories created/verified")

def start_frontend():
    """Start the Flask frontend."""
    print("🚀 Starting Asset Data Privacy Web Frontend...")
    print()
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check OpenAI key
    check_openai_key()
    
    # Create directories
    create_directories()
    
    print()
    print("🌐 Starting web server...")
    print("   Frontend will be available at: http://localhost:5001")
    print("   Press Ctrl+C to stop the server")
    print()
    
    try:
        # Start the Flask app
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_frontend()
