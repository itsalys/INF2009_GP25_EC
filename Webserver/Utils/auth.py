import jwt
import datetime
import os
from flask import request, jsonify
from Models.admin import Admin
from Models.employee import Employee
from dotenv import load_dotenv

load_dotenv()  # Load SECRET_KEY from .env

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in .env file")

# Function to generate JWT token
def generate_jwt(user_id, role):
    """Generates a JWT token for authentication."""
    payload = {
        "id": user_id,
        "role": role,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=5)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Function to verify JWT token and return user
def verify_token(required_role):
    """Verifies JWT token and checks if the user has the correct role."""
    token = request.headers.get("Authorization")
    if not token:
        return None, jsonify({"error": "Unauthorized. Missing token"}), 401

    try:
        token = token.split(" ")[1]  # Remove "Bearer " prefix
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        if decoded["role"] != required_role:
            return None, jsonify({"error": f"Unauthorized. {required_role} access required"}), 403

        if required_role == "admin":
            user = Admin.query.get(decoded["id"])
        else:
            user = Employee.query.get(decoded["id"])

        if not user:
            return None, jsonify({"error": "Invalid token"}), 403
        return user, None

    except jwt.ExpiredSignatureError:
        return None, jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return None, jsonify({"error": "Invalid token"}), 403
