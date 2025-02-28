from flask import Blueprint, request, jsonify
from Controllers.employee_controller import (
    get_all_employees,
    get_employee_by_id,
    add_employee,
    update_employee,
    delete_employee
)
from Utils.auth import verify_token  

employees_bp = Blueprint("employees", __name__)

# Admin: Get all employees
@employees_bp.route("/", methods=["GET"])
def get_employees():
    admin, error = verify_token("admin")  
    if error:
        return error

    employees = get_all_employees()
    return jsonify(employees)

# Employee/Admin: Get employee by ID
@employees_bp.route("/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    user, error = verify_token("admin")  
    if error:
        user, error = verify_token("employee")  
        if error or user.employee_id != employee_id:
            return jsonify({"error": "Unauthorized access"}), 403

    employee, error = get_employee_by_id(employee_id)
    if error:
        return jsonify({"error": error}), 404

    return jsonify(employee)

# Admin: Add a new employee
@employees_bp.route("/", methods=["POST"])
def create_employee():
    admin, error = verify_token("admin")  
    if error:
        return error

    data = request.get_json()
    message, error = add_employee(data)

    if error:
        return jsonify({"error": error}), 400

    return jsonify({"message": message}), 201

# Admin: Update employee details
@employees_bp.route("/<int:employee_id>", methods=["PUT"])
def modify_employee(employee_id):
    admin, error = verify_token("admin")  
    if error:
        return error

    data = request.get_json()
    message, error = update_employee(employee_id, data)

    if error:
        return jsonify({"error": error}), 404

    return jsonify({"message": message})

# Admin: Delete an employee
@employees_bp.route("/<int:employee_id>", methods=["DELETE"])
def remove_employee(employee_id):
    admin, error = verify_token("admin")  
    if error:
        return error

    message, error = delete_employee(employee_id)

    if error:
        return jsonify({"error": error}), 404

    return jsonify({"message": message})
