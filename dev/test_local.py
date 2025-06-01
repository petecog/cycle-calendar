#!/usr/bin/env python3
"""
Local test script for UCI MTB calendar sync
"""

import os
import sys
from calendar_generator import CalendarGenerator

def test_calendar_generation():
    """Test calendar generation locally"""
    print("🧪 Testing UCI MTB Calendar Generation")
    print("=" * 40)
    
    try:
        generator = CalendarGenerator()
        success = generator.generate_ical_file('test_calendar.ics')
        
        if success and os.path.exists('test_calendar.ics'):
            file_size = os.path.getsize('test_calendar.ics')
            print(f"✅ Calendar generated successfully!")
            print(f"📄 File: test_calendar.ics ({file_size} bytes)")
            
            # Read and display first few lines
            with open('test_calendar.ics', 'r', encoding='utf-8') as f:
                lines = f.readlines()[:10]
                print(f"📝 First 10 lines:")
                for i, line in enumerate(lines, 1):
                    print(f"   {i:2d}: {line.rstrip()}")
            
            print(f"\n📊 Total lines: {len(f.readlines()) + 10}")
            return True
        else:
            print("❌ Calendar generation failed")
            return False
            
    except Exception as e:
        print(f"💥 Error during testing: {e}")
        return False

if __name__ == "__main__":
    success = test_calendar_generation()
    sys.exit(0 if success else 1)