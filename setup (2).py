#!/usr/bin/env python3
"""
Setup script for AI Game Bot Complete Standalone
Installs all dependencies and prepares the application
"""

import subprocess
import sys
import os

def install_requirements():
    """Install all required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False
    return True

def main():
    print("🚀 Setting up AI Game Bot Complete Standalone...")
    
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return
    
    if install_requirements():
        print("✅ Setup complete!")
        print("🎮 Run 'python AI_GameBot_Standalone.py' to start the application")
    else:
        print("❌ Setup failed!")

if __name__ == "__main__":
    main()
