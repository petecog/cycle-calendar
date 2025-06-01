#!/usr/bin/env python3
"""
Browser Automation for UCI Excel Downloads

Uses Playwright to automate real browser interactions with the UCI website
to download Excel calendar files, bypassing protection mechanisms.
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional, List
import logging
from playwright.async_api import async_playwright, Page, Download

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UCIBrowserDownloader:
    """Browser automation for UCI Excel downloads"""
    
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path(__file__).parent.parent / 'data'
        self.output_dir.mkdir(exist_ok=True)
        
    async def download_year(self, year: str, headless: bool = True) -> bool:
        """
        Download UCI Excel file for a specific year using browser automation
        
        Args:
            year: Year to download (e.g. "2025") 
            headless: Whether to run browser in headless mode
            
        Returns:
            True if successful, False otherwise
        """
        
        logger.info(f"🤖 Starting browser automation for UCI {year} calendar...")
        
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(
                headless=headless,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-extensions'
                ]
            )
            
            # Create context with realistic settings
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
            )
            
            page = await context.new_page()
            
            try:
                # Navigate to UCI calendar
                logger.info(f"📡 Navigating to UCI calendar page...")
                await page.goto(
                    "https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB",
                    wait_until="domcontentloaded",
                    timeout=60000
                )
                
                # Wait for page to fully load and content to appear
                logger.info(f"⏳ Waiting for page content to load...")
                await page.wait_for_timeout(5000)
                
                # Handle cookie consent and overlays
                await self._handle_overlays(page)
                
                # Take a screenshot for debugging
                await page.screenshot(path=self.output_dir / f"debug_page_loaded_{year}.png")
                logger.info(f"✅ UCI page loaded successfully")
                
                # Handle year selection if needed
                await self._handle_year_selection(page, year)
                
                # Find and click download elements
                download_success = await self._trigger_excel_download(page, year)
                
                if download_success:
                    logger.info(f"✅ Successfully downloaded {year} UCI calendar")
                    return True
                else:
                    logger.error(f"❌ Failed to download {year} UCI calendar")
                    return False
                    
            except Exception as e:
                logger.error(f"❌ Browser automation error: {e}")
                return False
                
            finally:
                await browser.close()
    
    async def _handle_overlays(self, page: Page) -> None:
        """Handle cookie consent and other overlays that might block interactions"""
        
        logger.info(f"🍪 Checking for overlays (cookies, popups, etc.)...")
        
        try:
            # Cookie consent patterns
            cookie_selectors = [
                '#cookiescript_accept',
                '#cookiescript_accept_all',
                'button:has-text("Accept")',
                'button:has-text("Accept All")',
                'button:has-text("OK")',
                '[data-testid="accept-cookies"]',
                '.cookie-accept',
                '.accept-cookies'
            ]
            
            for selector in cookie_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element and await element.is_visible():
                        logger.info(f"🍪 Found cookie consent: {selector}")
                        await element.click()
                        await page.wait_for_timeout(1000)
                        logger.info(f"✅ Accepted cookies")
                        break
                except Exception as e:
                    continue
            
            # Close any remaining overlays
            overlay_selectors = [
                '[aria-label="Close"]',
                'button:has-text("Close")',
                '.modal-close',
                '.popup-close',
                '.overlay-close'
            ]
            
            for selector in overlay_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element and await element.is_visible():
                        logger.info(f"❌ Found overlay close button: {selector}")
                        await element.click()
                        await page.wait_for_timeout(500)
                except Exception as e:
                    continue
                    
            # Wait a bit for overlays to disappear
            await page.wait_for_timeout(2000)
            
        except Exception as e:
            logger.warning(f"⚠️  Overlay handling error (continuing): {e}")
    
    async def _handle_year_selection(self, page: Page, year: str) -> None:
        """Handle year selection in UCI interface"""
        
        logger.info(f"🔍 Checking for year selection (target: {year})...")
        
        try:
            # Look for year selector elements
            year_selectors = [
                f'option[value="{year}"]',
                f'text="{year}"',
                f'[data-year="{year}"]',
                f'button:has-text("{year}")'
            ]
            
            for selector in year_selectors:
                element = await page.query_selector(selector)
                if element:
                    logger.info(f"📅 Found year selector: {selector}")
                    await element.click()
                    await page.wait_for_timeout(1000)
                    return
            
            logger.info(f"ℹ️  No year selector found - assuming current year is displayed")
            
        except Exception as e:
            logger.warning(f"⚠️  Year selection error (continuing): {e}")
    
    async def _trigger_excel_download(self, page: Page, year: str) -> bool:
        """Trigger Excel file download"""
        
        logger.info(f"🔍 Looking for Excel download elements...")
        
        try:
            # Look for download button/link patterns
            download_selectors = [
                'text="Download season"',
                'text="Download"',
                '[aria-label*="Download"]',
                'a[href*="excel"]',
                'a[href*=".xls"]',
                'button:has-text("Download")',
                '.download-button',
                '#download-button'
            ]
            
            download_element = None
            for selector in download_selectors:
                element = await page.query_selector(selector)
                if element:
                    logger.info(f"📥 Found download element: {selector}")
                    download_element = element
                    break
            
            if not download_element:
                logger.error(f"❌ Could not find download button")
                # Take screenshot for debugging
                await page.screenshot(path=self.output_dir / f"debug_no_download_button_{year}.png")
                return False
            
            # Set up download handler
            async with page.expect_download(timeout=30000) as download_info:
                logger.info(f"🖱️  Clicking download button...")
                await download_element.click()
                
                # Look for XLS/Excel specific option
                await page.wait_for_timeout(1000)
                
                excel_selectors = [
                    'text="xls"',
                    'text="Excel"', 
                    'a[href*=".xls"]',
                    '[data-format="xls"]'
                ]
                
                for selector in excel_selectors:
                    excel_element = await page.query_selector(selector)
                    if excel_element:
                        logger.info(f"📊 Found Excel format option: {selector}")
                        await excel_element.click()
                        break
            
            # Handle the download
            download = await download_info.value
            
            # Save the file
            output_file = self.output_dir / f"{year}.xls"
            await download.save_as(output_file)
            
            # Verify download
            if output_file.exists() and output_file.stat().st_size > 0:
                file_size = output_file.stat().st_size
                logger.info(f"✅ Download saved: {output_file} ({file_size} bytes)")
                return True
            else:
                logger.error(f"❌ Download failed or file empty")
                return False
                
        except Exception as e:
            logger.error(f"❌ Download trigger error: {e}")
            # Take screenshot for debugging
            await page.screenshot(path=self.output_dir / f"debug_download_error_{year}.png")
            return False
    
    async def download_multiple_years(self, years: List[str], headless: bool = True) -> dict:
        """
        Download multiple years sequentially
        
        Args:
            years: List of years to download
            headless: Whether to run browser in headless mode
            
        Returns:
            Dictionary with year -> success status
        """
        
        results = {}
        
        logger.info(f"🚀 Starting bulk download for years: {', '.join(years)}")
        
        for year in years:
            logger.info(f"\n📅 Processing year {year}...")
            success = await self.download_year(year, headless)
            results[year] = success
            
            # Add delay between downloads to be respectful
            if len(years) > 1:
                logger.info(f"⏸️  Waiting 3 seconds before next download...")
                await asyncio.sleep(3)
        
        # Summary
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        
        logger.info(f"\n📊 Download Summary:")
        logger.info(f"   Total attempts: {total}")
        logger.info(f"   Successful: {successful}")
        logger.info(f"   Failed: {total - successful}")
        
        for year, success in results.items():
            status = "✅" if success else "❌"
            logger.info(f"   {status} {year}")
        
        return results

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
    """Main entry point for browser automation"""
    
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
    
    # Create downloader and run
    downloader = UCIBrowserDownloader()
    
    if len(years) == 1:
        success = await downloader.download_year(years[0], headless)
        sys.exit(0 if success else 1)
    else:
        results = await downloader.download_multiple_years(years, headless)
        # Exit with error if no downloads succeeded
        success_count = sum(1 for success in results.values() if success)
        sys.exit(0 if success_count > 0 else 1)

if __name__ == "__main__":
    asyncio.run(main())