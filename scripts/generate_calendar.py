#!/usr/bin/env python3
"""
Main script to generate UCI MTB calendar files
This is the entry point used by GitHub Actions
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from uci_calendar import CalendarGenerator, HTMLGenerator, UCIExcelParser

def main():
    """Generate both iCal and HTML calendar files using Excel data"""
    print("🚀 Starting UCI MTB Calendar generation...")
    
    success_count = 0
    
    # Load events from Excel file (required)
    excel_file = Path(__file__).parent.parent / '.claude' / 'UCICompetitions_MTB_2025.xls'
    
    if not excel_file.exists():
        print("❌ ERROR: UCI Excel file not found!")
        print(f"📄 Expected file: {excel_file}")
        print("💡 Please download UCICompetitions_MTB_2025.xls from UCI website")
        print("   and place it in the .claude/ folder")
        return 3
    
    print("📊 Loading events from UCI Excel file...")
    parser = UCIExcelParser()
    events = parser.parse_excel_file(str(excel_file))
    
    if not events:
        print("❌ ERROR: Failed to parse Excel file!")
        print("💡 The Excel file may be corrupted or have a different format")
        return 4
    
    print(f"✅ Loaded {len(events)} events from Excel file")
    
    # Filter for upcoming events
    upcoming_events = parser.get_upcoming_events()
    print(f"📅 {len(upcoming_events)} upcoming events")
    events = upcoming_events
    
    # Generate iCal file
    print("📅 Generating iCal file...")
    cal_generator = CalendarGenerator()
    cal_generator.events = events  # Set Excel events
    
    if cal_generator.generate_ical_file('calendar.ics'):
        print("✅ iCal file generated successfully")
        success_count += 1
    else:
        print("❌ Failed to generate iCal file")
        return 5
    
    # Generate HTML debug view
    print("🔧 Generating HTML debug view...")
    html_generator = HTMLGenerator()
    html_generator.events = events  # Set Excel events
    
    if html_generator.generate_html_calendar('debug.html'):
        print("✅ HTML debug view generated successfully")
        success_count += 1
    else:
        print("❌ Failed to generate HTML debug view")
        # Don't fail for HTML issues, iCal is the main output
    
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