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
    
    # Load events from ALL available Excel files in data directory
    data_dir = Path(__file__).parent.parent / 'data'
    existing_files = list(data_dir.glob("*.xls")) + list(data_dir.glob("*.xlsx"))
    
    # Filter out git.keep and other non-data files
    excel_files = [f for f in existing_files if f.name != 'git.keep' and not f.name.startswith('.')]
    
    if not excel_files:
        print("❌ ERROR: No UCI Excel files found!")
        print(f"📁 Searched directory: {data_dir}")
        # Try to download files
        try:
            import subprocess
            
            download_script = Path(__file__).parent / 'download_uci_excel.py'
            result = subprocess.run(['python', str(download_script), 'all'], 
                                  capture_output=True, text=True, timeout=60)
            
            # Check if any files were downloaded
            excel_files = [f for f in data_dir.glob("*.xls") if f.name != 'git.keep']
            excel_files.extend([f for f in data_dir.glob("*.xlsx") if f.name != 'git.keep'])
            
            if excel_files:
                print("✅ Successfully downloaded UCI Excel files!")
            else:
                print("❌ Automatic download failed")
                print("\n💡 Manual download instructions:")
                print("1. Visit: https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB")
                print("2. Click 'Download season' → 'xls'")
                print("3. Save as: data/YYYY.xls (e.g., data/2025.xls)")
                print("\n💡 Alternatively, add any UCI Excel file to data/ folder")
                return 3
                
        except Exception as e:
            print(f"❌ Download error: {e}")
            print("\n💡 Manual download instructions:")
            print("1. Visit: https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB")
            print("2. Click 'Download season' → 'xls'")
            print("3. Save as: data/YYYY.xls (e.g., data/2025.xls)")
            print("\n💡 Alternatively, add any UCI Excel file to data/ folder")
            return 3
    
    # Sort files by name for consistent processing order
    excel_files.sort(key=lambda f: f.name)
    
    print(f"\n📁 Found {len(excel_files)} UCI Excel file(s):")
    for i, file in enumerate(excel_files, 1):
        file_size = file.stat().st_size
        file_date = file.stat().st_mtime
        from datetime import datetime
        file_date_str = datetime.fromtimestamp(file_date).strftime("%Y-%m-%d %H:%M")
        print(f"   {i}. {file.name} ({file_size:,} bytes, modified: {file_date_str})")
    
    print(f"\n🔄 Combining events from all {len(excel_files)} files for comprehensive calendar")
    
    print("📊 Loading events from UCI Excel file(s)...")
    parser = UCIExcelParser()
    
    # Always use multiple file parsing for consistency
    events = parser.parse_multiple_files([str(f) for f in excel_files])
    
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
    
    # Generate in templates directory for local serving
    templates_dir = Path(__file__).parent.parent / 'src' / 'uci_calendar' / 'templates'
    debug_html_path = templates_dir / 'debug.html'
    
    if html_generator.generate_html_calendar(str(debug_html_path)):
        print("✅ HTML debug view generated successfully")
        success_count += 1
        
        # Copy calendar.ics to templates directory for local serving
        try:
            import shutil
            calendar_ics_path = templates_dir / 'calendar.ics'
            shutil.copy2('calendar.ics', str(calendar_ics_path))
            print("📋 Calendar file copied to templates directory for local serving")
        except Exception as e:
            print(f"⚠️  Warning: Could not copy calendar.ics to templates: {e}")
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