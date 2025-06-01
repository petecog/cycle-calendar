#!/usr/bin/env python3
"""
Browser Automation for UCI Excel Downloads - CLI Interface

Command-line interface for the UCI browser downloader package.
Uses the uci_calendar.browser_downloader module for actual implementation.
"""

import asyncio
import sys
from pathlib import Path
from typing import List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

def discover_available_years() -> List[str]:
    """Discover available years to download"""
    
    from datetime import datetime
    current_year = datetime.now().year
    
    # Try current year and next 2 years (UCI often has future seasons)
    years = [
        str(current_year),
        str(current_year + 1),
        str(current_year + 2)
    ]
    
    logger.info(f"🔍 Target years for download: {', '.join(years)}")
    return years

async def main():
    """Main entry point for browser automation CLI"""
    
    try:
        from uci_calendar import UCIBrowserDownloader, download_uci_year, download_uci_bulk
    except ImportError as e:
        logger.error(f"❌ Could not import uci_calendar package: {e}")
        logger.error("💡 Make sure you're running from the project root and have installed dependencies")
        sys.exit(1)
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['all', 'auto', 'bulk']:
            # Download all available years
            years = discover_available_years()
            mode = "bulk"
        else:
            # Download specific year
            years = [sys.argv[1]]
            mode = "single"
    else:
        # Default: current year only
        from datetime import datetime
        years = [str(datetime.now().year)]
        mode = "default"
    
    # Check for headless mode flag
    headless = not ('--visible' in sys.argv or '--head' in sys.argv)
    
    logger.info(f"🚀 UCI Browser Downloader starting...")
    logger.info(f"   Mode: {mode}")
    logger.info(f"   Years: {', '.join(years)}")
    logger.info(f"   Headless: {headless}")
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / 'data'
    
    # Run downloads
    if len(years) == 1:
        success = await download_uci_year(years[0], output_dir, headless)
        sys.exit(0 if success else 1)
    else:
        results = await download_uci_bulk(years, output_dir, headless)
        # Exit with error if no downloads succeeded
        success_count = sum(1 for success in results.values() if success)
        sys.exit(0 if success_count > 0 else 1)

if __name__ == "__main__":
    asyncio.run(main())