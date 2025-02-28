import bcrypt
from Models.employee import Employee
from Models import db

def get_all_employees():
    """Retrieve all employees."""
    employees = Employee.query.all()
    return [{"id": emp.employee_id, "name": emp.full_name, "email": emp.email} for emp in employees]

def get_employee_by_id(employee_id):
    """Retrieve an employee by ID."""
    employee = Employee.query.get(employee_id)
    if not employee:
        return None, "Employee not found"
    
    return {
        "id": employee.employee_id,
        "name": employee.full_name,
        "email": employee.email,
        "department": employee.department
    }, None

def add_employee(data):
    """Add a new employee with hashed password."""
    hashed_password = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    new_employee = Employee(
        full_name=data["full_name"],
        department=data["department"],
        profile_pic=data.get("profile_pic"),
        email=data["email"],
        password=hashed_password
    )

    db.session.add(new_employee)
    db.session.commit()
    return "Employee added successfully", None

def update_employee(employee_id, data):
    """Update employee details."""
    employee = Employee.query.get(employee_id)
    if not employee:
        return None, "Employee not found"

    employee.full_name = data.get("full_name", employee.full_name)
    employee.department = data.get("department", employee.department)
    employee.email = data.get("email", employee.email)

    db.session.commit()
    return "Employee updated successfully", None

def delete_employee(employee_id):
    """Delete an employee."""
    employee = Employee.query.get(employee_id)
    if not employee:
        return None, "Employee not found"

    db.session.delete(employee)
    db.session.commit()
    return "Employee deleted successfully", None
