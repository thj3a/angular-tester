#!/usr/bin/env python3

import subprocess
import sys
import os

def is_chrome_installed():
    """Check if Chrome/Chromium is installed"""
    browsers = ['google-chrome', 'chromium', 'chromium-browser', 'google-chrome-stable']
    for browser in browsers:
        try:
            subprocess.run([browser, '--version'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
            return browser
        except FileNotFoundError:
            continue
    return None

def install_chrome():
    """Install Chromium browser"""
    try:
        # Try to install using apt (Debian/Ubuntu)
        print("Installing Chromium browser...")
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'chromium-browser'], check=True)
        return 'chromium-browser'
    except subprocess.CalledProcessError:
        print("Failed to install Chromium using apt")
        return None
    except FileNotFoundError:
        # Try yum (Red Hat/CentOS/Fedora)
        try:
            subprocess.run(['sudo', 'yum', 'install', '-y', 'chromium'], check=True)
            return 'chromium'
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Failed to install Chromium using yum")
            return None

def ensure_chrome():
    """Ensure Chrome/Chromium is available"""
    chrome_path = is_chrome_installed()
    if chrome_path:
        print(f"Chrome/Chromium found: {chrome_path}")
        return chrome_path
    
    print("Chrome/Chromium not found. Attempting to install...")
    chrome_path = install_chrome()
    if chrome_path:
        print(f"Successfully installed: {chrome_path}")
        return chrome_path
    else:
        print("Failed to install Chrome/Chromium")
        return None

if __name__ == "__main__":
    chrome = ensure_chrome()
    if chrome:
        print(f"Ready to use: {chrome}")
    else:
        print("Chrome/Chromium is not available")
        sys.exit(1)