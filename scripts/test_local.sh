#!/bin/bash
# Local testing script for test-deployment branch
# Run this script to test changes before merging to main

set -e  # Exit on any error

echo "🧪 UCI MTB Calendar - Local Testing Script"
echo "==========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "scripts/generate_calendar.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if we're on test-deployment branch
current_branch=$(git branch --show-current)
if [ "$current_branch" != "test-deployment" ]; then
    echo "⚠️  Warning: You're on branch '$current_branch', not 'test-deployment'"
    echo "   This script is designed for testing on the test-deployment branch"
    read -p "   Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

echo "🔧 Step 1: Activating development environment..."
if [ ! -d "venv-dev" ]; then
    echo "❌ Error: venv-dev not found. Please run ./scripts/setup_dev.sh first"
    exit 1
fi

# Activate environment
source activate_dev.sh

echo ""
echo "📊 Step 2: Generating calendar files..."
python scripts/generate_calendar.py

if [ $? -ne 0 ]; then
    echo "❌ Error: Calendar generation failed"
    exit 1
fi

echo ""
echo "🔍 Step 3: Verifying generated files..."
if [ ! -f "src/uci_calendar/templates/debug.html" ]; then
    echo "❌ Error: debug.html not found in templates directory"
    exit 1
fi

if [ ! -f "src/uci_calendar/templates/calendar.ics" ]; then
    echo "❌ Error: calendar.ics not found in templates directory"
    exit 1
fi

echo "✅ Files generated successfully:"
echo "   - src/uci_calendar/templates/debug.html"
echo "   - src/uci_calendar/templates/calendar.ics"
echo "   - calendar.ics (root directory)"

echo ""
echo "🚀 Step 4: Starting local web server..."
echo "   URL: http://localhost:8000"
echo "   Debug page: http://localhost:8000/debug.html"
echo "   Calendar file: http://localhost:8000/calendar.ics"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""

cd src/uci_calendar/templates
python -m http.server 8000