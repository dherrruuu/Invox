"""Settings / company profile route."""
from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from src.invox.services.company_service import CompanyService

from .auth import login_required

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")


@settings_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    svc = CompanyService()
    if request.method == "POST":
        fields = {
            "company_name": request.form.get("company_name", "").strip(),
            "address": request.form.get("address", "").strip(),
            "phone_number": request.form.get("phone_number", "").strip(),
            "email": request.form.get("email", "").strip(),
            "gst_number": request.form.get("gst_number", "").strip(),
            "bank_details": request.form.get("bank_details", "").strip(),
            "terms_and_conditions": request.form.get("terms_and_conditions", "").strip(),
        }
        svc.update_profile(**fields)
        flash("Company profile saved.", "success")
        return redirect(url_for("settings.index"))

    profile = svc.get_profile()
    return render_template("settings.html", profile=profile, user=session["user"])
