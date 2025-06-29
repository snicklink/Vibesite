#!/usr/bin/env python3
"""
Build script to create standalone executable
"""

import subprocess
import sys
import os

def install_pyinstaller():
    print("Installing PyInstaller...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])

def build_executable():
    print("Building standalone executable...")
    
    # PyInstaller command to create standalone app
    cmd = [
        'pyinstaller',
        '--onefile',                    # Single executable file
        '--windowed',                   # No console window
        '--name=VibegameUpdater',       # App name
        '--icon=images/snick_vibe_logo.png',  # App icon (if exists)
        'update-site.py'
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n✅ SUCCESS!")
        print("Your standalone app is ready:")
        print("📁 Location: dist/VibegameUpdater")
        print("🎯 Just double-click it to run!")
        print("\nNo more 'python update-site.py' - just click and go!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print("Trying without icon...")
        
        # Try again without icon
        cmd_no_icon = [
            'pyinstaller',
            '--onefile',
            '--windowed',
            '--name=VibegameUpdater',
            'update-site.py'
        ]
        subprocess.check_call(cmd_no_icon)
        print("\n✅ SUCCESS!")
        print("Your standalone app is ready:")
        print("📁 Location: dist/VibegameUpdater")
        print("🎯 Just double-click it to run!")

if __name__ == "__main__":
    try:
        install_pyinstaller()
        build_executable()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Run this manually:")
        print("pip install pyinstaller")
        print("pyinstaller --onefile --windowed --name=VibegameUpdater update-site.py")