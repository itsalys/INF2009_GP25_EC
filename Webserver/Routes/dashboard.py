from flask import Blueprint, render_template, session, redirect, url_for
from Controllers.attendance_controller import get_all_attendance

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/admin/dashboard")
def admin_dashboard():
    # Ensure only admins can access
    if session.get("role") != "admin":
        return redirect(url_for("auth.admin_login"))

    # Fetch only clocked-in employees
    attendance_records = [
        record for record in get_all_attendance() if record["clocked_in"]
    ]

    return render_template("admin_dashboard.html", attendance_records=attendance_records, role="admin")
