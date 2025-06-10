#!/bin/bash

# WebLens Quick Setup Script
# This script sets up the WebLens testing framework using conda

set -e

echo "🚀 WebLens Setup Script (Conda)"
echo "==============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if conda is available
print_status "Checking conda installation..."
if ! command -v conda &> /dev/null; then
    print_error "Conda is not installed or not in PATH"
    print_status "Please install Miniconda or Anaconda:"
    print_status "  - Miniconda: https://docs.conda.io/en/latest/miniconda.html"
    print_status "  - Anaconda: https://www.anaconda.com/download"
    exit 1
fi

conda_version=$(conda --version)
print_success "Conda found: $conda_version"

# Check if we're in a conda environment
if [[ "$CONDA_DEFAULT_ENV" != "" && "$CONDA_DEFAULT_ENV" != "base" ]]; then
    print_success "Conda environment detected: $CONDA_DEFAULT_ENV"
    read -p "Do you want to update the current environment? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Updating current conda environment..."
        if conda env update -f environment.yml; then
            print_success "Environment updated successfully"
        else
            print_error "Failed to update conda environment"
            exit 1
        fi
    else
        print_status "Skipping environment update"
    fi
elif [[ "$CONDA_DEFAULT_ENV" == "base" ]]; then
    print_warning "You're in the base conda environment"
    read -p "Create new 'weblens' environment? (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        print_status "Creating new conda environment 'weblens'..."
        if conda env create -f environment.yml; then
            print_success "Conda environment 'weblens' created"
            print_warning "Please activate the environment:"
            echo "  conda activate weblens"
            echo "  ./setup.sh"
            exit 0
        else
            print_error "Failed to create conda environment"
            exit 1
        fi
    fi
else
    print_status "Creating new conda environment 'weblens'..."
    if conda env create -f environment.yml; then
        print_success "Conda environment 'weblens' created"
        print_warning "Please activate the environment:"
        echo "  conda activate weblens"
        echo "  ./setup.sh"
        exit 0
    else
        print_error "Failed to create conda environment"
        exit 1
    fi
fi

# Check Python version (in current environment)
print_status "Checking Python version in current environment..."
python_version=$(python --version 2>&1 | cut -d' ' -f2)

if python -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
    print_success "Python $python_version is compatible"
else
    print_error "Python 3.9+ is required. Current version: $python_version"
    exit 1
fi

# Browser Use Cloud API doesn't need local browser installation

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    print_status "Creating .env file from template..."
    cp .env.example .env
    print_success ".env file created"
    print_warning "Please edit .env file and add your API keys"
else
    print_status ".env file already exists"
fi

# Create required directories
print_status "Creating required directories..."
mkdir -p logs screenshots videos reports browser_profiles
print_success "Directories created"

# Test the installation
print_status "Testing the installation..."
if python -c "import weblens; print('WebLens imported successfully')"; then
    print_success "WebLens framework is ready!"
else
    print_error "Installation test failed"
    exit 1
fi

# Run a quick test
print_status "Running quick validation test..."
if python weblens_cli.py profiles list > /dev/null 2>&1; then
    print_success "CLI is working correctly"
else
    print_warning "CLI test had issues, but basic installation seems OK"
fi

echo
echo "🎉 Setup Complete!"
echo "=================="
echo
echo "Next steps:"
echo "1. Edit .env file with your Browser-use API key"
echo "2. Run example tests: python weblens_cli.py run examples/basic_tests.py"
echo "3. Check available profiles: python weblens_cli.py profiles list"
echo "4. Read the documentation: cat README.md"
echo
echo "Quick commands:"
echo "• Run tests: make run-examples"
echo "• List profiles: make profiles-list"
echo "• Get help: python weblens_cli.py --help"
echo
print_success "Happy testing with WebLens! 🚀"
