#!/usr/bin/env python3
"""
Open the filtered URL in browser for manual inspection
"""

import webbrowser
import time

def open_filtered_url():
    """Open the filtered UCI URL in browser"""
    
    # The filtered URL with all our parameters
    filtered_url = "https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB&seasonId=1002&raceCategory=ME%2CME%2CWE%2CMM%2CWM%2CXE&raceType=END%2CDHI%2CXCR%2CXCE%2CXCC%2CXCM%2CXCO"
    
    print("🌐 Opening filtered UCI MTB calendar URL...")
    print(f"🔗 URL: {filtered_url}")
    print()
    print("📋 Filter parameters:")
    print("   - Discipline: MTB (Mountain Bike)")
    print("   - Season: 1002 (likely 2025)")
    print("   - Categories: ME,WE,MM,WM,XE (Men/Women Elite, Masters, Mixed)")
    print("   - Race Types: END,DHI,XCR,XCE,XCC,XCM,XCO")
    print("     * END: Enduro")
    print("     * DHI: Downhill")  
    print("     * XCR: Cross-Country Relay")
    print("     * XCE: Eliminator")
    print("     * XCC: Cross-Country Short Track")
    print("     * XCM: Marathon")
    print("     * XCO: Cross-Country Olympic")
    print()
    print("💡 After the page loads and events appear:")
    print("   1. Scroll down to load all events")
    print("   2. Save the page (Ctrl+S) as 'UCI_Filtered_Calendar.html'")
    print("   3. Place it in .claude/ folder for testing")
    
    webbrowser.open(filtered_url)

if __name__ == "__main__":
    open_filtered_url()