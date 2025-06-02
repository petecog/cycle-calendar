#!/bin/bash
# Quick activation script for deploy environment
echo "🔧 Activating UCI MTB Calendar deploy environment..."
source venv-deploy/bin/activate
echo "✅ Virtual environment activated (venv-deploy)!"
echo ""
echo "🚀 Available deployment commands:"
echo "   python scripts/generate_calendar.py # Generate calendar files"
echo "   python scripts/download_uci_excel.py # Download UCI data"
echo ""
echo "📊 Production tools:"
echo "   python scripts/browser_download_uci.py # Browser-based download"
echo ""
echo "💡 To deactivate: deactivate"
