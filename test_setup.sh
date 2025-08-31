#!/bin/bash

echo "Testing environment setup..."

# Check Python version
python3 --version

# Create virtual environment
python3 -m venv test_env

# Activate virtual environment and install dependencies
source test_env/bin/activate && pip install requests pytest

# Test building the package
source test_env/bin/activate && python setup.py sdist bdist_wheel

echo "Test completed successfully"