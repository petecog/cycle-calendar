#!/bin/bash
# Local development environment setup for UCI MTB Calendar Sync
# Creates isolated Python virtual environment

set -e  # Exit on any error

echo "🚀 Setting up UCI MTB Calendar Sync local development environment"
echo "================================================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "📦 Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing production dependencies..."
pip install -r requirements.txt

echo "🛠️  Installing development dependencies..."
pip install -r requirements-dev.txt

# Create activation script for convenience
cat > activate_dev.sh << 'EOF'
#!/bin/bash
# Quick activation script for development environment
echo "🔧 Activating UCI MTB Calendar development environment..."
source venv/bin/activate
echo "✅ Virtual environment activated!"
echo ""
echo "🧪 Available commands:"
echo "   python test_local.py              # Test scraping locally"
echo "   python calendar_generator.py      # Generate iCal file"
echo "   python html_calendar_generator.py # Generate HTML debug view"
echo "   python serve_local.py             # Start local web server"
echo ""
echo "🎨 Code quality:"
echo "   black .                           # Format code"
echo "   flake8 .                          # Lint code"
echo "   pytest                            # Run tests"
echo ""
echo "💡 To deactivate: deactivate"
EOF

chmod +x activate_dev.sh

echo ""
echo "✅ Local development environment setup complete!"
echo ""
echo "📝 To use the environment:"
echo "   source venv/bin/activate"
echo "   # OR use the convenience script:"
echo "   source activate_dev.sh"
echo ""
echo "🧪 To test the setup:"
echo "   source venv/bin/activate"
echo "   python test_local.py"
echo ""
echo "🌐 To start local server:"
echo "   source venv/bin/activate"
echo "   python serve_local.py"
echo ""
echo "🎯 VS Code users:"
echo "   1. Open Command Palette (Ctrl+Shift+P)"
echo "   2. 'Python: Select Interpreter'"
echo "   3. Choose './venv/bin/python'"