#!/usr/bin/env python3
"""
Simple local server for testing - uses Python's built-in server
"""

import os
import sys
import webbrowser
from pathlib import Path

def start_simple_server(port=8000):
    """Start simple HTTP server"""
    
    # Ensure we're in the right directory
    os.chdir(Path(__file__).parent)
    
    # Generate files if missing
    if not os.path.exists('debug.html'):
        print("🔧 Generating debug.html...")
        try:
            sys.path.append(str(Path(__file__).parent.parent / 'src'))
            from uci_calendar import HTMLGenerator
            generator = HTMLGenerator()
            generator.generate_html_calendar()
        except Exception as e:
            print(f"⚠️  Could not generate debug.html: {e}")
    
    print(f"🚀 Starting simple server on port {port}...")
    print(f"📄 Main page: http://localhost:{port}/")
    print(f"🔧 Debug view: http://localhost:{port}/debug.html")
    print(f"📅 Calendar: http://localhost:{port}/calendar.ics")
    print(f"\n💡 Press Ctrl+C to stop")
    
    # Try to open browser
    try:
        webbrowser.open(f'http://localhost:{port}')
    except:
        pass
    
    # Use Python's built-in server
    try:
        import subprocess
        subprocess.run([sys.executable, '-m', 'http.server', str(port)])
    except KeyboardInterrupt:
        print(f"\n👋 Server stopped")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    start_simple_server(args.port)