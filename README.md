# 🚵‍♂️ UCI MTB Calendar Sync

Automatically syncs [UCI MTB calendar](https://www.uci.org/calendar/mtb/1voMyukVGR4iZMhMlDfRv0?discipline=MTB) events to a Google Calendar-compatible format.

## 📅 Quick Start

**Subscribe to the calendar:**
```
https://petecog.github.io/cycle-calendar/calendar.ics
```

**View events online:**
- [Main Page](https://petecog.github.io/cycle-calendar/) - Subscription instructions
- [Debug View](https://petecog.github.io/cycle-calendar/debug.html) - Live event listing

## 🔄 How it works

1. **GitHub Actions** runs weekly (Sundays 6 AM UTC)
2. **Processes** UCI Excel files from multiple seasons (2025.xls, 2026.xls, etc.)
3. **Generates** an iCal (.ics) file + HTML debug view from 655+ events
4. **Deploys** to GitHub Pages automatically

**Current Status**: 385 upcoming events from combined 2025+2026 seasons

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
python dev/serve_simple.py --port 3000  # Start local server
python dev/test_local.py                # Test scraping  
python scripts/generate_calendar.py     # Generate all files
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
│       ├── excel_parser.py  # UCI Excel file parser (multi-file support)
│       ├── calendar_generator.py # iCal file generator
│       ├── html_generator.py # HTML debug viewer
│       └── templates/       # HTML templates
├── scripts/                  # Executable utilities
│   ├── generate_calendar.py # Main generation script (multi-file)
│   ├── download_uci_excel.py # UCI Excel download (manual fallback)
│   └── setup_dev.sh        # Development setup
├── data/                    # UCI Excel files
│   ├── 2025.xls            # 651 events
│   ├── 2026.xls            # 4 events
│   └── [future files auto-included]
├── .claude/                 # Knowledge management
│   ├── memory/             # Session summaries
│   ├── scratch/            # Experimental code
│   └── input/              # User-shared files
├── docs/                    # Documentation
├── index.html              # GitHub Pages main page
├── .github/workflows/       # CI/CD automation (weekly schedule)
└── .devcontainer/          # VSCode dev environment
```

## 🚀 Deployment

See [docs/SETUP.md](docs/SETUP.md) for detailed deployment instructions.

## 📋 TODOs - Automated UCI Excel Downloads

**Current Status**: Manual Excel download → Automatic processing  
**Goal**: Fully automated pipeline without manual intervention

### Immediate Next Steps (Branch: `feature/uci-auth`)

1. **🤖 Browser Automation Approach**
   - Implement Selenium/Playwright to automate real browser
   - Navigate to UCI calendar page 
   - Locate and click "Download season" → "xls" buttons
   - Process downloaded files automatically
   - **Advantage**: Bypasses Cloudflare/bot protection by using real browser

2. **🔄 Hybrid Fallback System**
   - Try browser automation first
   - Fall back to existing Excel files if automation fails
   - Notify via GitHub Actions if manual download needed
   - **Implementation**: Enhanced GitHub Actions workflow with intelligent fallback

3. **🎯 Virtual Browser Integration**
   - Headless Chrome/Firefox automation
   - Full JavaScript execution context
   - Handle dynamic content loading
   - **Research**: puppeteer, playwright, selenium-wire options

### Advanced Future Options

4. **🔍 Session Context Replication**
   - Visit UCI calendar page first to establish browser context
   - Extract any hidden tokens/cookies
   - Replay exact browser session for API access

5. **📡 Alternative UCI Data Sources**
   - Investigate other UCI API endpoints
   - Monitor for UCI website changes that might re-enable direct access
   - Consider UCI RSS feeds or other public data sources

**Investigation Completed**: 
- ✅ HAR file analysis (no authentication required)
- ✅ Direct API replication (blocked by protection layer)
- ✅ Protection mechanisms identified (Cloudflare, geographic restrictions)
- ✅ Fallback workflow confirmed reliable

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