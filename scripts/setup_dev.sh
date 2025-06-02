#!/bin/bash
# Environment setup for UCI MTB Calendar Sync
# Supports separate development and deployment environments

set -e  # Exit on any error

# Parse command line arguments
SETUP_MODE="both"
if [[ "$1" == "--dev" ]]; then
    SETUP_MODE="dev"
elif [[ "$1" == "--deploy" ]]; then
    SETUP_MODE="deploy"
elif [[ -n "$1" ]]; then
    echo "❌ Invalid option: $1"
    echo "Usage: $0 [--dev|--deploy]"
    echo "  No flag: Set up both development and deployment environments"
    echo "  --dev: Set up only development environment (venv-dev/)"
    echo "  --deploy: Set up only deployment environment (venv-deploy/)"
    exit 1
fi

echo "🚀 Setting up UCI MTB Calendar Sync environment(s)"
echo "================================================================="
echo "📋 Setup mode: $SETUP_MODE"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Function to setup an environment
setup_environment() {
    local env_name="$1"
    local requirements_file="$2"
    local venv_dir="venv-${env_name}"
    
    echo ""
    echo "🔧 Setting up ${env_name} environment..."
    echo "───────────────────────────────────────"
    
    # Create virtual environment
    if [ ! -d "$venv_dir" ]; then
        echo "📦 Creating virtual environment: $venv_dir"
        python3 -m venv "$venv_dir"
    else
        echo "📦 Virtual environment already exists: $venv_dir"
    fi
    
    # Activate virtual environment
    echo "🔧 Activating virtual environment..."
    source "$venv_dir/bin/activate"
    
    # Upgrade pip
    echo "⬆️  Upgrading pip..."
    pip install --upgrade pip
    
    # Install dependencies
    echo "📚 Installing $env_name dependencies from $requirements_file..."
    pip install -r "$requirements_file"
    
    # Create activation script
    local activate_script="activate_${env_name}.sh"
    cat > "$activate_script" << EOF
#!/bin/bash
# Quick activation script for $env_name environment
echo "🔧 Activating UCI MTB Calendar $env_name environment..."
source $venv_dir/bin/activate
echo "✅ Virtual environment activated ($venv_dir)!"
echo ""
EOF

    if [[ "$env_name" == "dev" ]]; then
        cat >> "$activate_script" << 'EOF'
echo "🧪 Available development commands:"
echo "   python scripts/generate_calendar.py # Generate calendar files"
echo "   python scripts/setup_test_data.py   # Set up test data"
echo "   cd src/uci_calendar/templates && python -m http.server 8000 # Start local web server"
echo ""
echo "🎨 Code quality:"
echo "   black .                           # Format code"
echo "   flake8 .                          # Lint code"
echo "   pytest                            # Run tests"
echo ""
echo "🧪 Pre-commit hooks:"
echo "   pre-commit install                # Install git hooks"
echo "   pre-commit run --all-files        # Run all hooks"
echo ""
EOF
    elif [[ "$env_name" == "deploy" ]]; then
        cat >> "$activate_script" << 'EOF'
echo "🚀 Available deployment commands:"
echo "   python scripts/generate_calendar.py # Generate calendar files"
echo "   python scripts/download_uci_excel.py # Download UCI data"
echo ""
echo "📊 Production tools:"
echo "   python scripts/browser_download_uci.py # Browser-based download"
echo ""
EOF
    fi
    
    cat >> "$activate_script" << 'EOF'
echo "💡 To deactivate: deactivate"
EOF
    
    chmod +x "$activate_script"
    
    # Deactivate environment
    deactivate
    
    echo "✅ $env_name environment setup complete!"
    echo "   Virtual environment: $venv_dir"
    echo "   Activation script: $activate_script"
}

# Setup environments based on mode
if [[ "$SETUP_MODE" == "both" || "$SETUP_MODE" == "dev" ]]; then
    setup_environment "dev" "requirements-dev.txt"
fi

if [[ "$SETUP_MODE" == "both" || "$SETUP_MODE" == "deploy" ]]; then
    setup_environment "deploy" "requirements.txt"
fi

echo ""
echo "🎉 Environment setup complete!"
echo "================================================================="
echo ""
echo "📝 Usage instructions:"

if [[ "$SETUP_MODE" == "both" ]]; then
    echo "For development work:"
    echo "   source activate_dev.sh"
    echo ""
    echo "For deployment/production work:"
    echo "   source activate_deploy.sh"
elif [[ "$SETUP_MODE" == "dev" ]]; then
    echo "For development work:"
    echo "   source activate_dev.sh"
elif [[ "$SETUP_MODE" == "deploy" ]]; then
    echo "For deployment/production work:"
    echo "   source activate_deploy.sh"
fi

echo ""
echo "🧪 To test the setup:"
if [[ "$SETUP_MODE" == "both" || "$SETUP_MODE" == "dev" ]]; then
    echo "   source activate_dev.sh"
    echo "   python scripts/generate_calendar.py"
fi
if [[ "$SETUP_MODE" == "both" || "$SETUP_MODE" == "deploy" ]]; then
    echo "   source activate_deploy.sh"
    echo "   python scripts/generate_calendar.py"
fi

echo ""
echo "🌐 To start local web server:"
echo "   source activate_dev.sh  # (development environment recommended)"
echo "   cd src/uci_calendar/templates"
echo "   python -m http.server 8000"
echo "   # Then visit http://localhost:8000"

echo ""
echo "🎯 VS Code users:"
echo "   1. Open Command Palette (Ctrl+Shift+P)"
echo "   2. 'Python: Select Interpreter'"
echo "   3. Choose './venv-dev/bin/python' (for development)"
echo "   4. Or choose './venv-deploy/bin/python' (for deployment testing)"