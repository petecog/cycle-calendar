#!/bin/bash
# Test script for GitHub Actions acquisition logging

echo "📋 DATA ACQUISITION SUMMARY:"
echo "=============================="

# Count files and show details
excel_count=$(find data/ -name "*.xls" -o -name "*.xlsx" 2>/dev/null | wc -l)
echo "📊 Total Excel files available: $excel_count"

if [ $excel_count -gt 0 ]; then
  echo "📄 Available files:"
  for file in data/*.xls data/*.xlsx; do
    if [ -f "$file" ] 2>/dev/null; then
      filename=$(basename "$file")
      filesize=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null || echo "unknown")
      filedate=$(stat -c%y "$file" 2>/dev/null | cut -d' ' -f1 || stat -f%Sm -t%Y-%m-%d "$file" 2>/dev/null || echo "unknown")
      echo "   ✅ $filename (${filesize} bytes, modified: $filedate)"
    fi
  done
  
  # Determine acquisition method based on file timestamps
  echo ""
  echo "🔍 DATA ACQUISITION METHOD:"
  recent_files=$(find data/ -name "*.xls" -o -name "*.xlsx" -newermt "1 hour ago" 2>/dev/null | wc -l || echo "0")
  if [ $recent_files -gt 0 ]; then
    echo "   🤖 BROWSER AUTOMATION - Fresh files downloaded automatically"
    echo "   📡 Source: UCI website via Playwright browser automation"
    echo "   ⏰ Downloaded: Within last hour"
  else
    echo "   📁 EXISTING FILES - Using previously available data"
    echo "   📡 Source: Manual download or previous automation"
    echo "   ⏰ Last updated: More than 1 hour ago"
  fi
else
  echo "   ❌ NO DATA FILES - Calendar generation will fail"
fi

echo "=============================="