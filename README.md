# 🚵‍♂️ UCI MTB Calendar Sync

[![Calendar Feed](https://img.shields.io/badge/📅_Calendar_Feed-Subscribe-blue?style=for-the-badge&link=https://petecog.github.io/cycle-calendar/calendar.ics)](https://petecog.github.io/cycle-calendar/calendar.ics)

**Never miss a mountain bike race again!** This service automatically tracks all UCI Mountain Bike World Cup races, championships, and events, delivering them straight to your calendar app.

## 🎯 For Mountain Bike Fans

**What is this?** A free calendar subscription that puts all UCI mountain bike races directly in your phone or computer calendar. No more manually checking the UCI website or missing race announcements.

**What events do I get?** All official UCI Mountain Bike competitions:
- 🏆 **World Cup races** (Downhill, Cross-Country, Short Track)  
- 🌍 **World Championships** (Annual world titles)
- 🌎 **Continental Championships** (Europe, Americas, Asia, Africa, Oceania)
- 🚵‍♂️ **Major stage races** (Cape Epic, Leadville, and other UCI events)
- 👶 **Youth competitions** (Junior and U23 championships)

**How reliable is it?** Completely automated - updates weekly from UCI's official calendar. Built and maintained by mountain bike fans who actually use it.

## 📅 Quick Start

**Just want the calendar?** Copy this link and add it to your calendar app:
```
https://petecog.github.io/cycle-calendar/calendar.ics
```

**Using Google Calendar?** You can also add by calendar ID:
```
n5fp5b82serkhd45ffpf98v3lq5f7jhe@import.calendar.google.com
```

**Need help subscribing?** Visit: [petecog.github.io/cycle-calendar](https://petecog.github.io/cycle-calendar/) for step-by-step instructions

**Want to see what events are coming?** Check the [live event listing](https://petecog.github.io/cycle-calendar/debug.html)

## 🔄 How it works (Simple Version)

Every week, this system automatically:
1. **Downloads** the latest race schedules from UCI's official website  
2. **Processes** multiple years of data (currently 2025-2027) and removes duplicates
3. **Converts** everything into standard calendar format that any app can read
4. **Updates** the calendar file so your subscribed calendar gets the latest info

**The technical details:** Uses browser automation to download UCI Excel files, processes 655+ total events, generates iCal format, and runs on GitHub Actions every Sunday at 6 AM UTC.

**Current Status**: 385 upcoming events from combined 2025+2026+2027 seasons

## 📱 Adding to Your Calendar App

| App | How to Subscribe |
|-----|-------------|
| **Google Calendar** | Settings → Add calendar → From URL → Paste the link above |
| **Apple Calendar** | File → New Calendar Subscription → Paste the link above |
| **Outlook** | Add calendar → Subscribe from web → Paste the link above |
| **Phone Apps** | Look for "Add calendar" or "Subscribe to calendar" in settings |

**💡 Pro tip:** Most calendar apps check for updates automatically, so you'll get new races without doing anything once subscribed.

---

## 🛠️ For Developers

**Want to run this yourself or contribute?** The rest of this README is for developers who want to modify or deploy their own version.

### Development Setup

#### Quick Setup (VSCode Dev Container)
1. Install "Dev Containers" extension
2. Open project in VSCode
3. `F1` → "Dev Containers: Reopen in Container"
4. All dependencies auto-installed!

#### Local Setup (Dual Environment)
```bash
# One-time setup (creates both dev and deploy environments)
./scripts/setup_dev.sh

# OR set up specific environment:
./scripts/setup_dev.sh --dev      # Development only (testing, linting, etc.)
./scripts/setup_dev.sh --deploy   # Production only (minimal dependencies)

# Daily development usage
source activate_dev.sh               # Full dev environment
python scripts/generate_calendar.py  # Generate calendar from Excel files
black .                              # Format code
flake8 .                             # Lint code
pytest                               # Run tests

# Start local web server
cd src/uci_calendar/templates
python -m http.server 8000           # Serve files locally for testing
```

#### VS Code Integration
- **Automatic setup**: Opens with `venv-dev/bin/python` as default interpreter
- **Integrated tools**: Black formatting, flake8 linting, pytest testing
- **Clean explorer**: Virtual environment directories hidden

#### Available Tasks (VSCode)
- `Ctrl+Shift+P` → "Tasks: Run Task"
- Generate Calendar, Test Local, Format Code, Lint Code

### Project Structure

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

### Deployment

See [docs/SETUP.md](docs/SETUP.md) for detailed deployment instructions.

### System Status

**Current Status**: ✅ **FULLY AUTOMATED** - Complete browser automation pipeline working reliably

**What's automated:**
- ✅ **Playwright browser automation** downloads UCI Excel files (100% success rate)
- ✅ **Multi-season processing** (2025, 2026, 2027) with duplicate removal
- ✅ **Cookie consent handling** for UCI website
- ✅ **Intelligent fallback** to existing files if downloads fail
- ✅ **Weekly GitHub Actions** deployment (Sundays 6 AM UTC)

**Current data:**
- ✅ **655+ total events** from 3 seasons combined
- ✅ **385 upcoming events** in public calendar
- ✅ **Clean deployment** (build artifacts separate from source)
- ✅ **Comprehensive logging** for troubleshooting

### Future Feature Ideas

**Event Filtering** - Let users hide specific event types (training camps, youth events, etc.)  
**Other Cycling Disciplines** - Separate calendars for road cycling, track, BMX  
**Better Time Zones** - Localized event times instead of UTC  
**Event Details** - More detailed event descriptions and categories


### Troubleshooting

**For users:**
- **No events showing?** Check the [debug view](https://petecog.github.io/cycle-calendar/debug.html) to see if events exist
- **Calendar not updating?** Most apps check for updates every few hours - be patient
- **Wrong time zone?** All events are currently in UTC (this is a known limitation)

**For developers:**
- **Local testing fails?** Use `source activate_dev.sh` (not the old venv/bin/activate)
- **Environment issues?** Run `./scripts/setup_dev.sh --dev` to rebuild dev environment
- **Missing seasons?** Add UCI Excel files to `data/` directory (auto-detected)
- **Excel download blocked?** Use manual download - automation handles processing

### Contributing

Want to improve this? Here's how:

1. **Set up development environment** (see above)
2. **Test your changes** with `python dev/test_local.py`  
3. **Format code** with `black .`
4. **Generate calendar files** with `python scripts/generate_calendar.py`
5. **Submit pull request** with your improvements

**Ideas for contributions:** Better error handling, timezone support, event filtering, support for other cycling disciplines.

**Development environment notes:**
- Use `activate_dev.sh` for development work (testing, linting, formatting)
- Use `activate_deploy.sh` for production testing (minimal dependencies)
- VS Code automatically configured for the development environment

---

*Automatically updated weekly via GitHub Actions • 655 events from 2025+2026 seasons*