#!/usr/bin/env python3
"""
Main script to generate UCI MTB calendar files
This is the entry point used by GitHub Actions
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from uci_calendar import CalendarGenerator, HTMLGenerator

def main():
    """Generate both iCal and HTML calendar files"""
    print("🚀 Starting UCI MTB Calendar generation...")
    
    success_count = 0
    
    # Generate iCal file
    print("📅 Generating iCal file...")
    cal_generator = CalendarGenerator()
    if cal_generator.generate_ical_file('calendar.ics'):
        print("✅ iCal file generated successfully")
        success_count += 1
    else:
        print("❌ Failed to generate iCal file")
    
    # Generate HTML debug view
    print("🔧 Generating HTML debug view...")
    html_generator = HTMLGenerator()
    if html_generator.generate_html_calendar('debug.html'):
        print("✅ HTML debug view generated successfully")
        success_count += 1
    else:
        print("❌ Failed to generate HTML debug view")
    
    if success_count == 2:
        print("🎉 All files generated successfully!")
        return 0
    elif success_count == 1:
        print("⚠️  Some files generated with errors")
        return 1
    else:
        print("💥 Generation failed")
        return 2

if __name__ == "__main__":
    sys.exit(main())