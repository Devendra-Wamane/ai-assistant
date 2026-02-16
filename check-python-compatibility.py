#!/usr/bin/env python3
"""
Python Version Compatibility Checker for AI Assistant
Ensures the environment meets FastAPI 0.129.0 requirements
"""

import sys
import subprocess

# Minimum Python version required by FastAPI 0.129.0
MIN_PYTHON_VERSION = (3, 10, 0)
RECOMMENDED_PYTHON_VERSION = (3, 11, 0)

def check_python_version():
    """Check if current Python version is compatible"""
    current_version = sys.version_info[:3]
    
    print(f"🐍 Current Python version: {'.'.join(map(str, current_version))}")
    print(f"📋 Minimum required: {'.'.join(map(str, MIN_PYTHON_VERSION))}")
    print(f"⭐ Recommended: {'.'.join(map(str, RECOMMENDED_PYTHON_VERSION))}")
    print()
    
    if current_version < MIN_PYTHON_VERSION:
        print("❌ INCOMPATIBLE: Your Python version is too old!")
        print(f"   FastAPI 0.129.0 requires Python {'.'.join(map(str, MIN_PYTHON_VERSION))} or higher")
        print()
        print("🔧 Solutions:")
        print("   1. Upgrade Python: https://www.python.org/downloads/")
        print("   2. Use pyenv: pyenv install 3.11")
        print("   3. Use conda: conda create -n ai-assistant python=3.11")
        return False
    elif current_version < RECOMMENDED_PYTHON_VERSION:
        print("⚠️  COMPATIBLE but not optimal")
        print(f"   Consider upgrading to Python {'.'.join(map(str, RECOMMENDED_PYTHON_VERSION))} for best performance")
        return True
    else:
        print("✅ EXCELLENT: Your Python version is fully compatible!")
        return True

def check_fastapi_compatibility():
    """Check if FastAPI can be installed with current Python version"""
    try:
        # Try importing FastAPI to see if it's already installed
        import fastapi
        print(f"📦 FastAPI already installed: {fastapi.__version__}")
        return True
    except ImportError:
        print("📦 FastAPI not installed, checking compatibility...")
        try:
            # Test if FastAPI 0.129.0 can be installed
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "--dry-run", "fastapi==0.129.0"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ FastAPI 0.129.0 is compatible with your Python version")
                return True
            else:
                print("❌ FastAPI 0.129.0 is NOT compatible with your Python version")
                print("Error:", result.stderr)
                return False
        except subprocess.TimeoutExpired:
            print("⏰ Timeout checking FastAPI compatibility")
            return False
        except Exception as e:
            print(f"❌ Error checking FastAPI compatibility: {e}")
            return False

def main():
    print("🔍 AI Assistant - Python Compatibility Check")
    print("=" * 50)
    
    # Check Python version
    python_ok = check_python_version()
    print()
    
    # Check FastAPI compatibility if Python is OK
    if python_ok:
        fastapi_ok = check_fastapi_compatibility()
        print()
        
        if python_ok and fastapi_ok:
            print("🎉 SUCCESS: Your environment is ready for AI Assistant!")
            print("   Run: pip install -r requirements.txt")
        else:
            print("❌ ISSUES DETECTED: Please fix the above issues before proceeding")
            sys.exit(1)
    else:
        print("❌ CRITICAL: Python version incompatible")
        sys.exit(1)

if __name__ == "__main__":
    main()