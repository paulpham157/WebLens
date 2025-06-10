#!/bin/bash

# WebLens Quick Start with Conda
# This script quickly sets up and runs WebLens

set -e

echo "🚀 WebLens Quick Start"
echo "====================="

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

# Install Playwright browsers if needed
echo "🌐 Checking Playwright browsers..."
if ! playwright install --dry-run &> /dev/null; then
    echo "📥 Installing Playwright browsers..."
    playwright install
else
    echo "✅ Playwright browsers already installed"
fi

# Create .env file if needed
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "📝 Please edit .env file and add your Browser-use API key"
fi

# Create required directories
mkdir -p logs screenshots videos reports browser_profiles

echo
echo "🎉 WebLens is ready!"
echo "==================="
echo
echo "Quick commands to try:"
echo "• List profiles: python weblens_cli.py profiles list"
echo "• Run basic tests: python weblens_cli.py run examples/basic_tests.py"
echo "• Get help: python weblens_cli.py --help"
echo
echo "Environment: $CONDA_DEFAULT_ENV"
echo "Python: $(python --version)"
echo
echo "Happy testing! 🚀"
