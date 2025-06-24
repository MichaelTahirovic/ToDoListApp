#!/usr/bin/env python3
"""
Installation script for the To-Do List Application
This script helps set up the required dependencies.
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ Failed to install {package}")
        return False

def main():
    print("🚀 To-Do List Application - Installation Script")
    print("=" * 50)
    
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Required packages
    packages = [
        "tkcalendar",
        "pillow"
    ]
    
    print("\n📦 Installing required packages...")
    success_count = 0
    
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 Installation Summary:")
    print(f"Successfully installed: {success_count}/{len(packages)} packages")
    
    if success_count == len(packages):
        print("\n✅ Installation completed successfully!")
        print("\n🎉 You can now run the application with:")
        print("   python main.py")
        return True
    else:
        print("\n❌ Some packages failed to install.")
        print("Please try installing them manually:")
        print("   pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    main() 