# Dynamic UCI Downloader Enhancement - Update Summary

**Date**: January 6, 2025  
**Enhancement**: Multi-Season Dynamic Download System  

## Overview

Enhanced the UCI Excel download system from single-year static downloads to a dynamic multi-season approach with intelligent fallback handling and simplified filename conventions.

## Key Improvements

### 1. ✅ Simplified Filename Convention
- **Changed from**: `UCICompetitions_MTB_2025.xls`
- **Changed to**: `2025.xls`
- **Benefits**: Cleaner naming, easier multi-year management, consistent format

### 2. ✅ Smart Fallback System
- **Auto-detection**: Scans `data/` folder for any `.xls`/`.xlsx` files
- **Most recent**: Uses newest file if exact year not found
- **User-friendly**: Lists all found files for transparency
- **Repository-friendly**: Enables manual file addition to repo

### 3. ✅ Dynamic Multi-Season Downloader
- **Year discovery**: Automatically tries current year + 2 future years
- **Batch processing**: Downloads all available seasons in one command
- **Comprehensive reporting**: Shows success/failure for each season
- **File management**: Proper naming and size reporting

### 4. ✅ Enhanced Script Interface
```bash
# Download all available seasons (2025, 2026, 2027)
python scripts/download_uci_excel.py all

# Download specific year
python scripts/download_uci_excel.py 2025

# Default behavior (tries all seasons)
python scripts/download_uci_excel.py
```

## Technical Implementation

### Dynamic Year Detection
```python
from datetime import datetime
current_year = datetime.now().year

# Try current year and next 2 years (UCI often has future seasons)
potential_years = [
    str(current_year),
    str(current_year + 1), 
    str(current_year + 2)
]
```

### Smart Fallback Logic
```python
# Check for any existing Excel files in data folder as fallback
data_dir = excel_file.parent
existing_files = list(data_dir.glob("*.xls")) + list(data_dir.glob("*.xlsx"))

if existing_files:
    # Use the most recent file as fallback
    latest_file = max(existing_files, key=lambda f: f.stat().st_mtime)
    excel_file = latest_file
```

### Multi-Season Download Architecture
- `download_uci_excel_for_year(year)` - Single year download
- `discover_available_years()` - Year detection logic
- `download_all_available_seasons()` - Batch download coordinator

## Updated Workflow

### Manual File Addition
1. Download UCI Excel file from website
2. Save as `data/YYYY.xls` (e.g. `data/2025.xls`)
3. Run `python scripts/generate_calendar.py`
4. System auto-detects and uses the file

### Automatic Discovery
1. Run `python scripts/download_uci_excel.py all`
2. System tries 2025, 2026, 2027 automatically
3. Downloads all available seasons with proper naming
4. Reports success/failure for each season

### Fallback Resilience
- Primary: Look for exact year (e.g. `2025.xls`)
- Secondary: Auto-detect any Excel files in `data/`
- Tertiary: Attempt dynamic download of all seasons
- Quaternary: Manual download instructions

## Integration Points

### Main Calendar Generator
- **Dynamic year detection**: Uses `datetime.now().year` instead of hardcoded "2025"
- **Enhanced fallback**: Lists all found Excel files before manual instructions
- **Multi-season download**: Calls `download_uci_excel.py all` for batch processing

### Test Data Setup
- **Updated for new naming**: Copies to `data/2025.xls` format
- **Year parameterization**: Accepts year argument for flexibility

## Benefits

### For Development
- ✅ **Easy testing**: Drop any UCI Excel file in `data/` folder
- ✅ **Multi-year support**: Handle multiple seasons simultaneously
- ✅ **Robust fallback**: Never fails if ANY Excel file exists

### For Production
- ✅ **Future-proof**: Automatically tries upcoming seasons
- ✅ **Repository integration**: Manual files can be committed to repo
- ✅ **Clear reporting**: Detailed feedback on download attempts

### For Maintenance
- ✅ **Simplified naming**: Consistent `YYYY.xls` format
- ✅ **Batch operations**: Download multiple seasons at once
- ✅ **Error resilience**: Graceful degradation with clear instructions

## Current Status

**Authentication Challenge**: UCI API requires Bearer token (Microsoft Azure AD, ~1 hour expiry)
- 🔐 API returns 403 Forbidden for unauthenticated requests
- 🎯 Framework ready for when authentication is solved
- 📚 Manual workflow remains primary method

**Testing Results**:
- ✅ Fallback system works perfectly (tested with `old_format.xls`)
- ✅ Dynamic year detection functional
- ✅ Multi-season attempt logic operational
- ✅ Proper error reporting and manual instructions

**File Structure**:
```
data/
├── git.keep              # Preserves directory
├── 2025.xls             # Current season (ignored by git)
├── 2026.xls             # Future season (if available)
└── any_other_file.xls    # Auto-detected as fallback
```

## Next Steps

1. **Authentication Research**: Investigate UCI Bearer token acquisition
2. **Season Discovery**: Enhance year detection by scraping UCI website
3. **Browser Automation**: Consider Selenium/Playwright for authenticated downloads
4. **Scheduled Updates**: GitHub Actions for automated daily downloads

This enhancement maintains backward compatibility while adding powerful multi-season capabilities and robust fallback handling.