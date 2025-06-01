# Scratch Directory

Experimental code, prototypes, and things we might revisit later.

## Purpose
- Store experimental implementations that don't belong in main codebase
- Preserve prototypes and proof-of-concept code
- Organize by topic/feature in subdirectories
- Keep exploratory work without polluting main code

## Organization
- Create subdirectories for different experiments
- Use descriptive folder names (e.g. `authentication-experiments/`, `alternative-parsers/`)
- Include README files in subdirectories to explain the experiment

## Examples
```
scratch/
├── authentication-experiments/
│   ├── azure-token-flow.py
│   └── selenium-download.py
├── alternative-parsers/
│   ├── pdf-parser.py
│   └── api-direct.py
└── ui-experiments/
    └── flask-web-interface.py
```

## Guidelines
- Code here may be incomplete or non-functional
- Document what was tried and why it was set aside
- Keep as reference for future approaches
- May be revisted when requirements change