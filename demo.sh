#!/bin/bash

# Demo script for Angular Tester

echo "Angular Tester Demo"
echo "==================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  pip install pytest
else
  echo "Activating virtual environment..."
  source venv/bin/activate
fi

echo ""
echo "To run the Angular Tester, you need to set the LLM_API_URL environment variable."
echo "Example:"
echo "export LLM_API_URL='https://your-llm-api.com/generate'"
echo ""
echo "Then run:"
echo "python angular_tester.py [directory]"
echo ""
echo "For example, to test the example Angular app:"
echo "export LLM_API_URL='https://your-llm-api.com/generate'"
echo "python angular_tester.py example-angular-app/src"