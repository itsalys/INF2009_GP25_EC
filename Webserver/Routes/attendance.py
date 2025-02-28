from flask import Blueprint, request, jsonify
from Models.attendance import Attendance
from Models.employee import Employee
from Models import db
from Utils.auth import verify_token

attendance_bp = Blueprint("attendance", __name__)

# Get all attendance records
@attendance_bp.route("/", methods=["GET"])
def get_attendance():
    admin, error = verify_token("admin")
    if error:
        return error  # Return error if authentication fails

    records = Attendance.query.all()
    return jsonify([
        {
            "id": rec.attendance_id,
            "employee_id": rec.employee_id,
            "timestamp": rec.timestamp.isoformat(),
            "clocked_in": rec.clocked_in
        }
        for rec in records
    ])
    
# Add an attendance record
@attendance_bp.route("/", methods=["POST"])
def add_attendance():
    data = request.get_json()

    # Validate request data
    if "employee_id" not in data or "clocked_in" not in data:
        return jsonify({"error": "Missing required fields: employee_id, clocked_in"}), 400

    # Check if employee exists
    employee = Employee.query.get(data["employee_id"])
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    new_record = Attendance(
        employee_id=data["employee_id"],
        clocked_in=data["clocked_in"]
    )
    db.session.add(new_record)
    db.session.commit()
    return jsonify({"message": "Attendance recorded"}), 201

# Employee: Get their own attendance records (Requires JWT)
@attendance_bp.route("/me", methods=["GET"])
def get_my_attendance():
    employee, error = verify_token("employee")
    if error:
        return error  # Return error if authentication fails

    records = Attendance.query.filter_by(employee_id=employee.employee_id).all()
    if not records:
        return jsonify({"error": "No attendance records found"}), 404

    return jsonify([
        {
            "id": rec.attendance_id,
            "timestamp": rec.timestamp.isoformat(),
            "clocked_in": rec.clocked_in
        }
        for rec in records
    ])
    
# Admin: Get attendance records for a specific employee (Requires admin JWT)
@attendance_bp.route("/<int:employee_id>", methods=["GET"])
def get_employee_attendance(employee_id):
    admin, error = verify_token("admin")
    if error:
        return error  # Return error if authentication fails

    records = Attendance.query.filter_by(employee_id=employee_id).all()

    if not records:
        return jsonify({"error": "No attendance records found for this employee"}), 404

    return jsonify([
        {
            "id": rec.attendance_id,
            "timestamp": rec.timestamp.isoformat(),  # Convert to ISO format
            "clocked_in": rec.clocked_in
        }
        for rec in records
    ])

# Admin: Update an employee's clock-in status and timestamp
@attendance_bp.route("/<int:attendance_id>", methods=["PUT"])
def update_attendance(attendance_id):
    admin, error = verify_token("admin")
    if error:
        return error  # Return error if authentication fails

    data = request.get_json()
    
    record = Attendance.query.get(attendance_id)
    if not record:
        return jsonify({"error": "Attendance record not found"}), 404

    # Validate and update fields
    if "clocked_in" in data:
        record.clocked_in = data["clocked_in"]

    if "timestamp" in data:
        try:
            from datetime import datetime
            record.timestamp = datetime.fromisoformat(data["timestamp"])
        except ValueError:
            return jsonify({"error": "Invalid timestamp format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS)"}), 400

    db.session.commit()
    return jsonify({"message": "Attendance record updated successfully"})
