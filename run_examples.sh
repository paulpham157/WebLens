#!/bin/bash
# Run WebLens examples

# Setup environment
echo "📋 Setting up environment..."
source ./setup.sh

# Display available examples
echo "🧪 Available examples:"
echo "1) Basic Natural Language Test"
echo "2) Login Test Example"
echo "3) Advanced Natural Language Assertions"
echo "4) Direct Browser-use API Example"
echo "5) Run All Examples"
echo "q) Quit"

# Choose example to run
read -p "Choose an example to run (1-5, or q to quit): " choice

case $choice in
    1)
        echo "🚀 Running Basic Natural Language Test..."
        python examples/natural_language_test.py
        ;;
    2)
        echo "🚀 Running Login Test Example..."
        python examples/login_test_example.py
        ;;
    3)
        echo "🚀 Running Advanced Natural Language Assertions..."
        python examples/advanced_natural_assertions.py
        ;;
    4)
        echo "🚀 Running Direct Browser-use API Example..."
        python examples/direct_browser_use.py
        ;;
    5)
        echo "🚀 Running All Examples..."
        echo "⏳ Running Basic Natural Language Test..."
        python examples/natural_language_test.py
        echo "⏳ Running Login Test Example..."
        python examples/login_test_example.py
        echo "⏳ Running Advanced Natural Language Assertions..."
        python examples/advanced_natural_assertions.py
        echo "⏳ Running Direct Browser-use API Example..."
        python examples/direct_browser_use.py
        ;;
    q|Q)
        echo "👋 Exiting..."
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo "✅ Examples executed successfully!"
