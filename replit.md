# INVOX

Billing and quotation management system for interior design, furniture manufacturing, plywood, and construction businesses.

## Stack

- **Backend**: Python 3.12 + Flask (web interface)
- **Database**: SQLite via SQLAlchemy ORM
- **PDF generation**: ReportLab
- **Original UI**: PyQt6 (desktop, replaced by Flask web app)

## Running the app

```bash
.venv/bin/python web_server.py
```

The workflow `INVOX Web` handles this automatically. The app runs on port 5000.

## Default login

- Username: `admin`
- Password: `admin123`

## Project structure

```
src/invox/          # Core business logic (untouched from original)
  models/           # SQLAlchemy ORM models
  services/         # Business logic (auth, invoice, customer, PDF, etc.)
  repositories/     # Data access layer
  db/               # SQLAlchemy engine + schema init
  utils/            # Formatting, validators

web/                # Flask web application
  __init__.py       # App factory
  routes/           # Blueprints: auth, dashboard, customers, products, invoices, quotations, settings
  templates/        # Jinja2 HTML templates (dark luxury theme)

web_server.py       # Entry point

tests/              # pytest test suite (service-layer coverage)
```

## Data directories

Created automatically under the project root:
- `Database/` — SQLite database (`invox.db`)
- `Bills/` — Generated invoice PDFs
- `Quotations/` — Generated quotation PDFs
- `Backup/`, `Reports/`, `Assets/`

## User preferences

- Keep the existing `src/invox/` service/model/db layer intact — all Flask routes call into those services.
- Dark luxury brand theme: background `#111111`, gold accent `#D4A373`, cards `#1E1E1E`.
- Python 3.12 (`.venv/bin/python`).
