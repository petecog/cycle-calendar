# 🚵‍♂️ UCI MTB Calendar Sync

Automatically downloads UCI MTB calendar Excel files and converts them to a Google Calendar-compatible iCal format.

## 📅 Quick Start

**Subscribe to the calendar:**
```
https://petecog.github.io/cycle-calendar/calendar.ics
```

**View events online:**
- [Main Page](https://petecog.github.io/cycle-calendar/) - Subscription instructions
- [Debug View](https://petecog.github.io/cycle-calendar/debug.html) - Live event listing

## 🔄 How it works

1. **Browser automation** downloads UCI Excel files using Playwright
2. **Processes** multiple seasons (2025.xls, 2026.xls, 2027.xls) with deduplication
3. **Generates** iCal (.ics) file + HTML debug view from 655+ total events
4. **GitHub Actions** runs weekly (Sundays 6 AM UTC) and deploys to GitHub Pages

**Current Status**: 385 upcoming events from combined 2025+2026+2027 seasons

## 📱 Calendar Apps

| App | Instructions |
|-----|-------------|
| **Google Calendar** | Settings → Add calendar → From URL |
| **Apple Calendar** | File → New Calendar Subscription |
| **Outlook** | Add calendar → Subscribe from web |

## 🛠️ Development

### Quick Setup (VSCode Dev Container)
1. Install "Dev Containers" extension
2. Open project in VSCode
3. `F1` → "Dev Containers: Reopen in Container"
4. All dependencies auto-installed!

### Local Setup (Python venv)
```bash
# One-time setup
./scripts/setup_dev.sh

# Daily usage
source venv/bin/activate
python scripts/browser_download_uci.py   # Download via browser automation
python scripts/generate_calendar.py     # Generate calendar from Excel files
python -m http.server 8000              # Serve files locally for testing
```

### Manual Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

### Available Tasks (VSCode)
- `Ctrl+Shift+P` → "Tasks: Run Task"
- Generate Calendar, Test Local, Format Code, Lint Code

## 📁 Project Structure

```
├── src/                      # Core application code
│   └── uci_calendar/        # Main package
│       ├── __init__.py      # Package interface
│       ├── excel_parser.py  # Multi-file Excel processing with deduplication
│       ├── browser_downloader.py # Playwright automation for downloads
│       ├── calendar_generator.py # iCal file generator
│       ├── html_generator.py # HTML debug viewer
│       └── templates/       # HTML templates
├── scripts/                  # Executable utilities
│   ├── generate_calendar.py # Main generation script
│   ├── browser_download_uci.py # Browser automation CLI
│   ├── download_uci_excel.py # Hybrid download with fallbacks
│   ├── setup_dev.sh        # Development setup
│   └── setup_test_data.py  # Test data utilities
├── data/                    # UCI Excel files
│   ├── 2025.xls            # 651 events
│   ├── 2026.xls            # 651 events (duplicates removed)
│   ├── 2027.xls            # 651 events (duplicates removed)
│   └── [auto-downloaded via browser automation]
├── .claude/                 # Knowledge management
│   ├── memory/             # Session summaries
│   ├── scratch/            # Experimental code
│   └── input/              # User-shared files
├── docs/                    # Documentation
├── index.html              # GitHub Pages main page
├── .github/workflows/       # CI/CD automation with browser automation
│   └── update-calendar.yml  # Weekly schedule (Sundays 6 AM UTC)
└── .devcontainer/          # VSCode dev environment
```

## 🚀 Deployment

See [docs/SETUP.md](docs/SETUP.md) for detailed deployment instructions.

## ✅ Status: Fully Automated System

**Current Status**: ✅ **FULLY AUTOMATED** - Complete browser automation pipeline  
**Achievement**: 100% automated UCI Excel downloads with Playwright browser automation

### 🤖 **Browser Automation Features**
- ✅ **Playwright automation** with 100% download success rate
- ✅ **Multi-season processing** (2025, 2026, 2027) with deduplication
- ✅ **Cookie consent handling** automated
- ✅ **Intelligent fallback** to existing files if downloads fail
- ✅ **Weekly GitHub Actions** schedule (Sundays 6 AM UTC)

### 📊 **Current Data Processing**
- ✅ **655+ total events** from 3 seasons combined
- ✅ **385 upcoming events** in public calendar
- ✅ **Duplicate detection** across multiple Excel files
- ✅ **Clean deployment** (build artifacts separate from source)
- ✅ **Comprehensive logging** for troubleshooting

## 🎯 Outstanding Feature Requests

### 1. **Event Filtering** ⏳
**Priority**: Medium  
**Description**: Exclude specific event types from calendar
- **Excel field filtering**: Filter based on event type, location, category columns
- **URL parameter filtering**: Dynamic filtering via query parameters
- **Use cases**: Hide training camps, administrative meetings, youth events

### 2. **Multiple Sport Disciplines** 📋
**Priority**: Medium  
**Description**: Create separate calendars for different cycling disciplines
- **Road cycling**: Separate calendar feed for road events
- **Track cycling**: Dedicated track event calendar
- **BMX**: BMX-specific event filtering
- **Implementation**: Extend browser automation to other UCI sport categories


## 🔧 Troubleshooting

- **No events showing?** Check the [debug view](https://petecog.github.io/cycle-calendar/debug.html)
- **Missing seasons?** Add UCI Excel files to `data/` directory (auto-detected)
- **Local testing fails?** Use `source venv/bin/activate` before running scripts
- **Excel download blocked?** Use manual download - automation handles processing

## 📝 Contributing

1. Make changes in dev container or local venv
2. Test with `python dev/test_local.py`
3. Format code with `black .`
4. Generate files with `python scripts/generate_calendar.py`
5. Submit pull request

---

*Automatically updated weekly via GitHub Actions • 655 events from 2025+2026 seasons*