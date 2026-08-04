---
name: INVOX web conversion
description: Flask web app added on top of existing PyQt6 desktop codebase; venv and run-command details.
---

# INVOX Web Conversion

**Why:** PyQt6 GUI cannot run headlessly on Replit; Flask web layer added so the app works in browser preview.

**How to apply:** All business logic stays in `src/invox/` (services, models, db) — untouched. The `web/` directory is the Flask layer only.

- Entry point: `web_server.py` → `web/__init__.py` (app factory)
- Workflow command: `.venv/bin/python web_server.py` (Flask/SQLAlchemy live in `.venv`, not the system Python)
- Templates: `web/templates/` — Jinja2, dark luxury theme (#111111 bg, #D4A373 gold)
- Routes: `web/routes/` — auth, dashboard, customers, products, invoices, quotations, settings

**Why .venv:** `installLanguagePackages` installs into `.venv`; the nix-wrapped system `python3` does NOT have flask on its path.
