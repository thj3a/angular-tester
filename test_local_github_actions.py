#!/usr/bin/env python3

"""
Simple test script to verify GitHub Actions workflow locally
"""

import os
import subprocess
import sys

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        raise

def main():
    print("Testing GitHub Actions workflow locally...")
    
    # Check if we have the required dependencies
    try:
        run_command("python --version")
        run_command("pip --version")
        run_command("pip list | grep -E '(requests|pytest)'")
    except subprocess.CalledProcessError:
        print("Failed to verify dependencies")
        return 1
    
    # Test if we can install requirements
    try:
        run_command("pip install -r requirements.txt")
        print("Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("Failed to install requirements")
        return 1
    
    # Test building the package
    try:
        run_command("python setup.py sdist bdist_wheel")
        print("Package built successfully")
    except subprocess.CalledProcessError:
        print("Failed to build package")
        return 1
    
    print("All tests passed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())