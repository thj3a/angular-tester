#!/usr/bin/env python3

print("Testing environment...")
import sys
print(f"Python version: {sys.version}")

try:
    import requests
    print("Requests module available")
except ImportError as e:
    print(f"Failed to import requests: {e}")

try:
    import pytest
    print("Pytest module available")
except ImportError as e:
    print(f"Failed to import pytest: {e}")

print("Environment test completed.")