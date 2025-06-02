# Setup Instructions

## 1. Create GitHub Repository

1. Go to GitHub and create a new repository called `cycle-calendar`
2. Make it public (required for GitHub Pages)
3. Don't initialize with README (we already have files)

## 2. Push Code to GitHub

```bash
git add .
git commit -m "Initial UCI MTB calendar sync implementation"
git branch -M main
git remote add origin https://github.com/YOURUSERNAME/cycle-calendar.git
git push -u origin main
```

## 3. Enable GitHub Pages

1. Go to your repository settings
2. Scroll down to "Pages" section
3. Source: Deploy from a branch
4. Branch: `gh-pages` (will be created automatically)
5. Save

## 4. Update URLs

Edit `index.html` and replace `yourusername` with your actual GitHub username:
- Change `https://yourusername.github.io/cycle-calendar/calendar.ics`
- To `https://YOURUSERNAME.github.io/cycle-calendar/calendar.ics`

## 5. Set Up Local Development (Optional)

### Environment Setup Options

```bash
# Set up both development and deployment environments
./scripts/setup_dev.sh

# OR set up specific environment:
./scripts/setup_dev.sh --dev      # Development only (testing, linting, etc.)
./scripts/setup_dev.sh --deploy   # Production only (minimal dependencies)
```

### Development Workflow

```bash
# Activate development environment
source activate_dev.sh

# Test the setup
python scripts/generate_calendar.py

# Run development tools
black .                    # Format code
flake8 .                   # Lint code
pytest                     # Run tests
pre-commit run --all-files # Run pre-commit hooks

# Start local web server
cd src/uci_calendar/templates
python -m http.server 8000
# Then visit http://localhost:8000
```

### VS Code Setup

The project includes VS Code configuration that automatically:
- Uses `venv-dev/bin/python` as the default interpreter
- Configures black for formatting and flake8 for linting
- Sets up pytest for testing
- Hides virtual environment directories from explorer

**Environment Types:**
- **Development** (`venv-dev/`): Full environment with testing, linting, browser automation
- **Production** (`venv-deploy/`): Minimal environment with only runtime dependencies

## 6. Trigger First Run

1. Go to Actions tab in your repository
2. Click "Update UCI MTB Calendar" workflow
3. Click "Run workflow" button
4. This will create the initial calendar file

## 7. Subscribe to Calendar

Once deployed, your calendar will be available at:
```
https://YOURUSERNAME.github.io/cycle-calendar/calendar.ics
```

## Troubleshooting

- **GitHub Pages not working?** Check that your repo is public
- **Workflow failing?** Check the Actions tab for error logs
- **Empty calendar?** The UCI site might have changed structure - check scraper.py
- **Local testing fails?** Make sure you have internet access to reach UCI site

## Customization

- Change update frequency: Edit `.github/workflows/update-calendar.yml` cron schedule
- Modify data processing: Edit `src/uci_calendar/excel_parser.py`
- Customize calendar metadata: Edit `src/uci_calendar/calendar_generator.py`
- Update web interface: Edit templates in `src/uci_calendar/templates/`
- Add new data sources: Extend parser or create new download scripts