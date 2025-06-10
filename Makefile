# WebLens Makefile
# Convenient commands for development and testing using conda

.PHONY: help install install-dev setup test test-unit test-integration test-e2e lint format clean run-examples

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install conda environment"
	@echo "  install-dev  - Install development dependencies"
	@echo "  setup        - Setup project"
	@echo "  test         - Run all tests"
	@echo "  test-unit    - Run unit tests only"
	@echo "  test-integration - Run integration tests"
	@echo "  test-e2e     - Run end-to-end tests"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code"
	@echo "  clean        - Clean up generated files"
	@echo "  run-examples - Run example tests"

# Installation targets
install:
	conda env create -f environment.yml

install-dev:
	conda env update -f environment.yml
	conda install -c conda-forge pytest pytest-asyncio pytest-mock

setup: 
	@echo "🚀 Setting up WebLens with conda..."
	@if ! command -v conda >/dev/null 2>&1; then \
		echo "❌ Conda not found. Please install Miniconda or Anaconda"; \
		exit 1; \
	fi
	@if [ "$$CONDA_DEFAULT_ENV" = "" ] || [ "$$CONDA_DEFAULT_ENV" = "base" ]; then \
		echo "⚠️  Please activate weblens conda environment first:"; \
		echo "   conda activate weblens"; \
		echo "   If environment doesn't exist, run: conda env create -f environment.yml"; \
		exit 1; \
	fi
	@echo "✅ WebLens setup complete!"
	@echo "📝 Don't forget to configure your .env file"

# Testing targets
test:
	pytest tests/ -v

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v --runslow

test-e2e:
	pytest tests/integration/ -v -m e2e --runslow

# Code quality targets
lint:
	flake8 weblens/ examples/ tests/
	mypy weblens/

format:
	black weblens/ examples/ tests/
	isort weblens/ examples/ tests/

# Cleanup targets
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/
	rm -rf logs/* screenshots/* videos/* reports/*

# Example execution
run-examples:
	@echo "🚀 Running basic examples..."
	python weblens_cli.py run examples/basic_tests.py --browsers chrome
	@echo "🎯 Running advanced examples..."
	python weblens_cli.py run examples/advanced_tests.py --browsers chrome --sequential

# Development helpers
dev-server:
	@echo "📱 Starting development environment..."
	@echo "Run tests with: make test"
	@echo "Run examples with: make run-examples"

# Profile management
profiles-list:
	python weblens_cli.py profiles list

profiles-create:
	python weblens_cli.py profiles create

# Quick test commands
smoke-test:
	python weblens_cli.py run examples/basic_tests.py --tags smoke --browsers chrome

regression-test:
	python weblens_cli.py run examples/basic_tests.py --tags regression --browsers chrome firefox

# CI/CD helpers
ci-test:
	pytest tests/unit/ -v --tb=short
	pytest tests/integration/ -v --tb=short -m "not slow"

# Documentation
docs:
	@echo "📚 WebLens Documentation"
	@echo "========================"
	@echo "📖 README: ./README.md"
	@echo "🔧 Examples: ./examples/"
	@echo "🧪 Tests: ./tests/"
	@echo "⚙️  CLI Help: python weblens_cli.py --help"

# Version management
version:
	@echo "📦 WebLens Version Information"
	@echo "=============================="
	@grep version pyproject.toml
	@python -c "import weblens; print(f'Installed version: {weblens.__version__}')"

# Environment check
check-env:
	@echo "🔍 Environment Check"
	@echo "==================="
	@python --version
	@echo "Python packages:"
	@pip list | grep -E "(browser-use|pytest)"
