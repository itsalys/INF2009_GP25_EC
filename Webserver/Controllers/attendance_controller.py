from flask import Blueprint, request, jsonify
from Controllers.attendance_controller import (
    get_all_attendance,
    get_employee_attendance,
    add_attendance,
    update_attendance
)
from Utils.auth import verify_token 

attendance_bp = Blueprint("attendance", __name__)

# Admin: Get all attendance records
@attendance_bp.route("/", methods=["GET"])
def fetch_attendance():
    admin, error = verify_token("admin")
    if error:
        return error

    records = get_all_attendance()
    return jsonify(records)

# Employee: Get their own attendance records
@attendance_bp.route("/me", methods=["GET"])
def fetch_my_attendance():
    employee, error = verify_token("employee")
    if error:
        return error

    records, error = get_employee_attendance(employee.employee_id)
    if error:
        return jsonify({"error": error}), 404

    return jsonify(records)

# Admin: Get attendance for a specific employee
@attendance_bp.route("/<int:employee_id>", methods=["GET"])
def fetch_employee_attendance(employee_id):
    admin, error = verify_token("admin") 
    if error:
        return error

    records, error = get_employee_attendance(employee_id)
    if error:
        return jsonify({"error": error}), 404

    return jsonify(records)

# Employee: Add attendance record (clock-in or clock-out)
@attendance_bp.route("/", methods=["POST"])
def record_attendance():
    employee, error = verify_token("employee") 
    if error:
        return error

    data = request.get_json()
    data["employee_id"] = employee.employee_id  # Ensure correct ID
    message, error = add_attendance(data)

    if error:
        return jsonify({"error": error}), 400

    return jsonify({"message": message}), 201

# Admin: Update attendance records (e.g., fix incorrect clock-in time)
@attendance_bp.route("/<int:attendance_id>", methods=["PUT"])
def modify_attendance(attendance_id):
    admin, error = verify_token("admin") 
    if error:
        return error

    data = request.get_json()
    message, error = update_attendance(attendance_id, data)

    if error:
        return jsonify({"error": error}), 404

    return jsonify({"message": message})
