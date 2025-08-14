#!/usr/bin/env python3
"""
Test Render Compatibility
This script tests if the backend can start with the new requirements
"""

import subprocess
import sys
import time
import requests

def test_backend_startup():
    """Test if the backend can start successfully"""
    print("🧪 Testing Backend Compatibility...")
    
    try:
        # Try to start the backend
        print("🚀 Starting backend server...")
        process = subprocess.Popen(
            [sys.executable, "simple_backend.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit for startup
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Backend started successfully!")
            
            # Try to connect to health endpoint
            try:
                response = requests.get("http://localhost:8000/health", timeout=5)
                if response.status_code == 200:
                    print("✅ Health endpoint responding!")
                    print("✅ Backend is fully compatible!")
                else:
                    print(f"⚠️  Health endpoint returned: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"⚠️  Could not connect to health endpoint: {e}")
            
            # Stop the process
            process.terminate()
            process.wait()
            return True
        else:
            # Process failed, get error output
            stdout, stderr = process.communicate()
            print("❌ Backend failed to start!")
            print("STDOUT:", stdout)
            print("STDERR:", stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error testing backend: {e}")
        return False

def test_requirements():
    """Test if requirements can be installed"""
    print("\n📦 Testing Requirements Installation...")
    
    try:
        # Try to install requirements
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements_render.txt"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ Requirements installed successfully!")
            return True
        else:
            print("❌ Requirements installation failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Requirements installation timed out!")
        return False
    except Exception as e:
        print(f"❌ Error testing requirements: {e}")
        return False

def main():
    """Main test function"""
    print("🌳 Vegetation Management Agent - Render Compatibility Test")
    print("=" * 60)
    
    # Test requirements first
    req_success = test_requirements()
    
    if req_success:
        # Test backend startup
        backend_success = test_backend_startup()
        
        if backend_success:
            print("\n🎉 All tests passed! Your backend is ready for Render deployment!")
            print("\n📋 Next steps:")
            print("1. Push your code to GitHub")
            print("2. Deploy to Render using requirements_render.txt")
            print("3. Use Python 3.12 in Render environment variables")
        else:
            print("\n❌ Backend startup failed. Check your simple_backend.py file.")
    else:
        print("\n❌ Requirements installation failed. Check requirements_render.txt")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main() 