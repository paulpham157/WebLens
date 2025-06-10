#!/bin/bash
# Quick Start: Login Test Example

echo "🚀 WebLens Login Test Quick Start"
echo "================================="

# Check if API key is set
if [ -z "$BROWSER_USE_API_KEY" ]; then
  echo "❓ BROWSER_USE_API_KEY environment variable not detected"
  
  # Check if .env file exists
  if [ -f .env ]; then
    echo "📁 Found .env file, loading configuration..."
    source .env
  else
    echo "❌ No .env file found"
    echo "Please create a .env file with your BROWSER_USE_API_KEY or set it now:"
    read -p "Enter your BROWSER_USE_API_KEY: " API_KEY
    
    if [ -z "$API_KEY" ]; then
      echo "❌ No API key provided. Exiting."
      exit 1
    else
      echo "BROWSER_USE_API_KEY=$API_KEY" > .env
      echo "✅ API key saved to .env file"
      export BROWSER_USE_API_KEY=$API_KEY
    fi
  fi
fi

# Check for conda environment
if command -v conda &>/dev/null; then
  echo "🐍 Conda detected, activating environment..."
  if conda env list | grep -q "weblens"; then
    conda activate weblens || source activate weblens
    echo "✅ Conda environment activated"
  else
    echo "⚠️ Weblens conda environment not found"
    echo "Creating new conda environment..."
    conda env create -f environment.yml
    conda activate weblens || source activate weblens
    echo "✅ Conda environment created and activated"
  fi
else
  echo "⚠️ Conda not detected, checking for Python dependencies..."
  if [ -f requirements.txt ]; then
    echo "📦 Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
  fi
fi

# Run the login test example
echo "🧪 Running login test example..."
echo "This will test login functionality on https://practicetestautomation.com/practice-test-login/"

python examples/login_test_example.py

echo "✅ Quick start complete!"
echo "For more examples, run: ./run_examples.sh"
echo "For documentation, see: docs/login_testing_guide.md"
