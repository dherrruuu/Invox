# INVOX

INVOX is a desktop billing and quotation management system for interior design, furniture manufacturing, plywood, and construction businesses. It uses SQLite, SQLAlchemy, and a branded desktop shell with login, dashboard summaries, customer/product masters, invoice and quotation generation, PDF export, and backup support.

## What is included

- Secure login with password hashing and a default `admin / admin123` account.
- SQLite-backed customer, product, invoice, quotation, company profile, and user models.
- Automatic invoice and quotation numbering.
- Invoice and quotation PDF generation with a branded template.
- Dashboard shell with navigation, summary cards, backup support, and settings placeholders.
- Compatibility shims so both `invox.*` and `src.invox.*` imports work in the workspace.

## Folders created automatically

If `D:/INVOX` is available, INVOX uses that path. Otherwise it falls back to `C:/Users/<user>/INVOX`.

- `Bills/`
- `Quotations/`
- `Customers/`
- `Database/`
- `Backup/`
- `Reports/`

## Setup

1. Create and activate a Python 3.12 environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python src/invox/main.py
```

If you prefer package execution after editable install:

```bash
python -m invox.main
```

## Default login

- Username: `admin`
- Password: `admin123`

## Sample output

The PDF generator writes invoices and quotations to the configured bills and quotations folders, for example:

- `INV-2026-0002.pdf`
- `QUO-2026-0002.pdf`

## Build notes

- The code base is structured for a future PyInstaller build.
- Use Python 3.12 for production packaging because the GUI stack is not guaranteed on alpha interpreters.