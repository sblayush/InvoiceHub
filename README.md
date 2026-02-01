# Seller Account Management

A small Python project to import, process and generate invoices/seller reports for marketplaces (Amazon, Flipkart, etc.). Provides CLI and web UI components and utilities to read orders, create invoices, and save outputs to Excel/JSON.

## Features
- Import orders from DB or local JSON/Excel inputs
- Generate marketplace-specific invoices (Amazon, Flipkart, Other)
- Save outputs to `output/` with per-date folders
- Simple Flask-based web UI under `web/` for viewing and editing invoices

## Prerequisites
- Python 3.8+ (3.9 recommended)
- pip

## Install

1. Create a virtual environment and activate it:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration
- Application credentials and settings live in the `properties/` folder:
  - `amazon_seller.credentials`, `flipkart_seller.credentials`, `seller.credentials`
  - `config.properties` and other `.properties` files used by utilities
- Python modules under `src/config/` expose helper functions to read these credentials.

Before running, ensure credential files and `config.properties` are populated with correct values.

## Data layout
- Inputs: `data/input/excel/` and `data/input/json/`
- Outputs: `output/excel/<date>/<vendor>/` and `output/logs/`

## Common commands

Run the main script:

```bash
python main.py
```

Start the web app (development):

```bash
python web/app.py
# or
python -m web.app
```

Create a local backup:

```bash
python TakeLocalBackup.py
```

## Project structure (key folders)
- `src/actions/` — marketplace-specific invoice generation logic
- `src/dao/` — DB access and persistence helpers
- `src/util/` — shared utilities (excel helpers, logging, GST state codes)
- `web/` — Flask app and frontend assets (`templates/`, `static/`)
- `properties/` — runtime configuration and credentials

## Development notes
- Review `main.py` to see top-level orchestration for batch runs.
- Look in `rough/` for older/experimental scripts and helpers.
- Unit tests are not included; consider adding tests under a `tests/` folder.

## Contributing
- Fork, create a branch, add tests for new functionality, and open a PR.

## License
Specify your license here (e.g., MIT) or add `LICENSE` to the repo.

---
If you want, I can also add a small `README` section describing how to populate the `properties/` credential files or generate a sample `.env`/example credentials file.
