from flask import jsonify, Blueprint, request, render_template, redirect, url_for, session
from Controllers.auth_controller import authenticate_admin, authenticate_employee

auth_bp = Blueprint("auth", __name__)

# Admin Login Route
@auth_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        token, error = authenticate_admin(email, password)
        if error:
            return render_template("admin_login.html", error=error)

        # Store token & role in session
        session["token"] = token
        session["role"] = "admin"
        return redirect(url_for("admin_dashboard"))

    return render_template("admin_login.html")

# Employee login
@auth_bp.route("/employee/login", methods=["POST"])
def employee_login():
    data = request.get_json()
    token, error = authenticate_employee(data["email"], data["password"])

    if error:
        return jsonify({"error": error}), 401

    return jsonify({"token": f"Bearer {token}"})
