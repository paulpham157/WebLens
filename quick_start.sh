#!/bin/bash

# WebLens Quick Start with Conda
# This script quickly sets up and runs WebLens with natural language testing

set -e

echo "🚀 WebLens Quick Start - Natural Language Browser Testing"
echo "======================================================"
echo "WebLens now uses natural language to control browsers!"

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Conda not found. Please install Miniconda or Anaconda first."
    echo "   Download from: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo "✅ Conda found"

# Check if weblens environment exists
if conda env list | grep -q "weblens"; then
    echo "✅ WebLens environment exists"
    echo "🔄 Activating environment..."
    eval "$(conda shell.bash hook)"
    conda activate weblens
else
    echo "📦 Creating WebLens environment..."
    conda env create -f environment.yml
    echo "🔄 Activating environment..."
    eval "$(conda shell.bash hook)"
    conda activate weblens
fi

# Browser Use Cloud API doesn't need local browser installation
echo "🌐 Using Browser Use Cloud API - no local browser installation needed"

# Check for API key
if [ ! -f .env ]; then
    echo "📝 Creating .env file for your API key"
    cp .env.example .env
    echo "📝 Please edit .env file and add your Browser-use API key"
fi

# Create required directories
mkdir -p logs screenshots videos reports browser_profiles

echo
echo "🎉 WebLens is ready with Natural Language Testing!"
echo "=============================================="
echo
echo "Quick commands to try:"
echo "• Run natural language test: python examples/natural_language_test.py"
echo "• Test login functionality: python examples/login_test_example.py"
echo "• Run all examples: ./run_examples.sh"
echo "• Get help: python weblens_cli.py --help"
echo
echo "📚 Documentation:"
echo "• Natural Language Guide: docs/natural_language_guide_full.md"
echo "• Login Testing Guide: docs/login_testing_guide.md"
echo
echo "Environment: $CONDA_DEFAULT_ENV"
echo "Python: $(python --version)"
echo
echo "Happy testing with natural language! 🚀"
