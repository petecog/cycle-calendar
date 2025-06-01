#!/usr/bin/env python3
"""
Local development server for UCI MTB Calendar Sync
Serves the calendar files and debug views on localhost
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

class CalendarHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve calendar files with proper MIME types"""
    
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def guess_type(self, path):
        """Set proper MIME type for .ics files"""
        result = super().guess_type(path)
        if isinstance(result, tuple) and len(result) == 2:
            mimetype, encoding = result
        else:
            mimetype, encoding = result, None
        
        if path.endswith('.ics'):
            return 'text/calendar', encoding
        return mimetype, encoding

def generate_files_if_missing():
    """Generate calendar files if they don't exist"""
    try:
        # Add src to path
        sys.path.append(str(Path(__file__).parent.parent / 'src'))
        
        # Generate iCal file if missing
        if not os.path.exists('calendar.ics'):
            print("📅 Generating calendar.ics...")
            from uci_calendar import CalendarGenerator
            generator = CalendarGenerator()
            generator.generate_ical_file()
        
        # Generate HTML debug view if missing
        if not os.path.exists('debug.html'):
            print("🔧 Generating debug.html...")
            from uci_calendar import HTMLGenerator
            html_generator = HTMLGenerator()
            html_generator.generate_html_calendar()
            
    except ImportError as e:
        print(f"⚠️  Could not generate files: {e}")
        print("💡 Make sure dependencies are installed: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error generating files: {e}")

def start_server(port=8000):
    """Start local development server"""
    
    # Ensure we're in the right directory
    os.chdir(Path(__file__).parent)
    
    # Generate files if they don't exist
    generate_files_if_missing()
    
    try:
        with socketserver.TCPServer(("", port), CalendarHTTPRequestHandler) as httpd:
            print(f"🚀 Starting local development server...")
            print(f"📍 Server running at: http://localhost:{port}")
            print(f"📄 Main page: http://localhost:{port}/")
            print(f"🔧 Debug view: http://localhost:{port}/debug.html")
            print(f"📅 Calendar file: http://localhost:{port}/calendar.ics")
            print(f"\n💡 Press Ctrl+C to stop the server")
            
            # Try to open browser
            try:
                webbrowser.open(f'http://localhost:{port}')
            except:
                pass
            
            httpd.serve_forever()
            
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use")
            print(f"💡 Try a different port: python serve_local.py --port 8001")
        else:
            print(f"❌ Server error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n👋 Server stopped")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Local development server for UCI MTB Calendar')
    parser.add_argument('--port', type=int, default=8000, help='Port to serve on (default: 8000)')
    parser.add_argument('--generate', action='store_true', help='Generate files and exit')
    
    args = parser.parse_args()
    
    if args.generate:
        generate_files_if_missing()
        print("✅ Files generated")
    else:
        start_server(args.port)