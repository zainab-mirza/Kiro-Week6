#!/usr/bin/env python3
"""
Setup script for BiteBalance (Free Version)
"""

import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def setup_env_file():
    """Setup .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        print("🔧 Creating .env file...")
        try:
            with open('.env.example', 'r') as example:
                content = example.read()
            with open('.env', 'w') as env_file:
                env_file.write(content)
            print("✅ .env file created! (No API key needed for free version)")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
        return True

def main():
    """Main setup function"""
    print("🥗 Setting up BiteBalance - The AI Menu Referee (FREE VERSION)")
    print("=" * 60)
    
    success = True
    
    # Install requirements
    if not install_requirements():
        success = False
    
    # Setup .env file
    if not setup_env_file():
        success = False
    
    if success:
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Run: streamlit run app.py")
        print("2. Your browser will open automatically")
        print("3. Start making better food choices! 🥗")
        print("\n💡 This free version uses intelligent mock AI - no API key needed!")
    else:
        print("\n❌ Setup encountered some issues. Please check the errors above.")

if __name__ == "__main__":
    main()