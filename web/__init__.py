"""INVOX Flask application factory."""
from __future__ import annotations

import os

from flask import Flask

from src.invox.db.connection import init_database
from src.invox.services.auth_service import AuthService


def create_app() -> Flask:
    from datetime import date

    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = os.environ.get("SESSION_SECRET", "invox-dev-secret-change-me")

    # Jinja2 globals
    app.jinja_env.globals["enumerate"] = enumerate

    @app.context_processor
    def inject_today():
        return {"today": str(date.today())}

    # Initialise DB, run migrations, seed default admin
    init_database()
    from src.invox.db.migrations import run_migrations
    run_migrations()
    auth = AuthService()
    auth.seed_default_admin()
    # Pre-fill company name if not set
    from src.invox.services.company_service import CompanyService as _CS
    _db = __import__("src.invox.db.connection", fromlist=["get_session"]).get_session()
    try:
        _prof = _CS(_db).get_profile()
        if not _prof.company_name or _prof.company_name == "INVOX Pvt Ltd":
            _CS(_db).update_profile(company_name="Balaji Wood Decor")
    finally:
        _db.close()

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.customers import customers_bp
    from .routes.dashboard import dashboard_bp
    from .routes.invoices import invoices_bp
    from .routes.payments import payments_bp
    from .routes.products import products_bp
    from .routes.quotations import quotations_bp
    from .routes.settings import settings_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(quotations_bp)
    app.register_blueprint(settings_bp)

    return app
