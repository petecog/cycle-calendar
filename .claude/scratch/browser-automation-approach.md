# Browser Automation Approach for UCI Excel Downloads

**Date**: June 1, 2025  
**Goal**: Implement virtual browser automation to download UCI Excel files automatically

## Approach Overview

Since direct API access is blocked by protection layers, use browser automation to simulate real user interactions with the UCI website.

## Recommended Technology Stack

### Option 1: Playwright (Recommended)
**Advantages**:
- Modern, fast, and reliable
- Built-in network interception
- Excellent headless support
- Cross-browser compatibility
- Easy file download handling

**Implementation**:
```python
from playwright.sync_api import sync_playwright

def download_uci_excel_with_browser(year: str, output_dir: Path) -> bool:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to UCI calendar
        page.goto("https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB")
        
        # Select year if needed
        if year != "2025":  # current year
            # Implement year selection logic
            pass
        
        # Wait for page to load completely
        page.wait_for_load_state("networkidle")
        
        # Set up download handling
        with page.expect_download() as download_info:
            # Click download button
            page.click('text="Download season"')
            page.click('text="xls"')
        
        download = download_info.value
        
        # Save file
        output_file = output_dir / f"{year}.xls"
        download.save_as(output_file)
        
        browser.close()
        return output_file.exists()
```

### Option 2: Selenium
**Advantages**:
- Well-established and stable
- Extensive documentation
- Wide browser support

**Disadvantages**:
- Slower than Playwright
- More complex setup
- Heavier resource usage

## Implementation Plan

### Phase 1: Basic Browser Automation
1. **Install Playwright**: Add to requirements-dev.txt
2. **Create browser downloader**: `scripts/browser_download_uci.py`
3. **Test manually**: Verify download works locally
4. **Integrate fallback**: Update `download_uci_excel.py` to try browser method

### Phase 2: GitHub Actions Integration
1. **Add browser dependencies**: Update GitHub Actions workflow
2. **Install browser binaries**: Playwright install chromium
3. **Test in CI environment**: Ensure headless mode works
4. **Add timeout handling**: Prevent stuck downloads

### Phase 3: Advanced Features
1. **Multi-year download**: Automate year selection
2. **Smart retry logic**: Handle temporary failures
3. **Download verification**: Check file size/content
4. **Error reporting**: Detailed failure notifications

## Technical Considerations

### 1. GitHub Actions Environment
```yaml
- name: Install Playwright
  run: |
    pip install playwright
    playwright install chromium

- name: Download UCI Excel files
  run: |
    python scripts/browser_download_uci.py all
```

### 2. File Download Detection
- Monitor download directory
- Check file completion
- Verify Excel file validity

### 3. Year Selection Logic
- Identify current year selection mechanism
- Implement year dropdown/navigation
- Handle dynamic content loading

### 4. Error Handling
- Network timeouts
- Missing elements
- Download failures
- Browser crashes

## Alternative Virtual Browser Approaches

### Puppeteer (Node.js)
- Could be integrated via subprocess
- Excellent Chrome DevTools integration
- Good for complex JavaScript interactions

### Selenium Grid
- Distributed browser testing
- Multiple browser instances
- Better for high-volume scenarios

### Browser API Extensions
- Chrome Extension approach
- Direct browser integration
- User-initiated automation

## Implementation Steps

### Step 1: Local Development Setup
```bash
# Add to requirements-dev.txt
playwright>=1.40.0

# Install and setup
pip install playwright
playwright install chromium

# Create test script
python scripts/test_browser_download.py
```

### Step 2: Core Browser Script
```python
#!/usr/bin/env python3
"""
Browser automation for UCI Excel downloads
Uses Playwright to automate real browser interactions
"""

import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
import logging

async def download_uci_season_browser(year: str) -> bool:
    """Download UCI season using browser automation"""
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']  # For CI
        )
        
        page = await browser.new_page()
        
        try:
            # Navigate to UCI calendar
            await page.goto(
                "https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB",
                wait_until="networkidle"
            )
            
            # Handle year selection if needed
            await handle_year_selection(page, year)
            
            # Trigger download
            download_path = await trigger_excel_download(page)
            
            return download_path is not None
            
        finally:
            await browser.close()

async def handle_year_selection(page, year: str):
    """Handle year selection in UCI interface"""
    # Implementation depends on UCI interface structure
    pass

async def trigger_excel_download(page):
    """Trigger Excel file download"""
    # Set up download handler
    async with page.expect_download() as download_info:
        # Click download elements
        await page.click('[aria-label="Download season"]')
        await page.click('text="xls"')
    
    download = await download_info.value
    return download
```

### Step 3: Integration with Existing System
- Update `download_uci_excel.py` to try browser method first
- Maintain fallback to manual process
- Add comprehensive logging

### Step 4: CI/CD Integration
- Update GitHub Actions workflow
- Add browser automation dependencies
- Test in cloud environment

## Success Criteria

1. **Automated downloads** working in local environment
2. **GitHub Actions integration** successful
3. **Multi-year support** functional
4. **Reliable fallback** to manual process
5. **Error handling** comprehensive

## Risk Mitigation

1. **UCI site changes**: Monitor for layout changes that break automation
2. **Rate limiting**: Respect rate limits, add delays between requests
3. **Browser detection**: Use realistic user-agent strings and timing
4. **Resource usage**: Optimize for GitHub Actions resource limits

This approach provides a robust path to full automation while maintaining the reliable manual fallback system.