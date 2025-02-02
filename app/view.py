from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.models import Employee
from app.cache import cache

api_bp = Blueprint("api", __name__)


@api_bp.route("/employees", methods=["GET"])
@swag_from(
    {
        "responses": {
            200: {
                "description": "List of employees",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "first_name": {"type": "string"},
                            "last_name": {"type": "string"},
                            "email": {"type": "string"},
                        },
                    },
                },
            }
        }
    }
)
@cache.cached(timeout=600)  # Cache for 10 minutes (600 seconds)
def get_employees():
    """Get all employees
    ---
    tags:
      - Employees
    """
    employees = Employee.get_all()
    return jsonify(
        [
            {
                "id": emp.id,
                "first_name": emp.first_name,
                "last_name": emp.last_name,
                "email": emp.email,
            }
            for emp in employees
        ]
    )


@api_bp.route("/employee/<int:emp_id>", methods=["GET"])
@swag_from(
    {
        "parameters": [
            {
                "name": "emp_id",
                "in": "path",
                "type": "integer",
                "required": True,
                "description": "Employee ID",
            }
        ],
        "responses": {
            200: {
                "description": "Employee details",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "email": {"type": "string"},
                    },
                },
            },
            404: {"description": "Employee not found"},
        },
    }
)
@cache.cached(
    timeout=600, key_prefix="employee_{emp_id}"
)  # Cache for 10 min per employee ID
def get_employee_by_id(emp_id):
    """Get an employee by ID
    ---
    tags:
      - Employees
    """
    employee = Employee.get_by_id(emp_id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    return (
        jsonify(
            {
                "id": employee.id,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "email": employee.email,
            }
        ),
        200,
    )


@api_bp.route("/employee", methods=["POST"])
@swag_from(
    {
        "tags": ["Employees"],
        "summary": "Add a new employee",
        "description": "Creates a new employee in the system.",
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "first_name": {
                            "type": "string",
                        },
                        "last_name": {
                            "type": "string",
                        },
                        "email": {"type": "string"},
                    },
                    "required": ["first_name", "last_name", "email"],
                },
            }
        ],
        "responses": {
            201: {
                "description": "Employee created successfully",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "example": 1},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "email": {"type": "string"},
                    },
                },
            },
            400: {
                "description": "Invalid input or email already exists",
                "schema": {
                    "type": "object",
                    "properties": {"error": {"type": "string"}},
                },
            },
        },
    }
)
def add_employee():
    """Add a new employee"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")

        if not first_name or not last_name or not email:
            return jsonify({"error": "Missing fields"}), 400

        new_employee = Employee.create(first_name, last_name, email)
        if not new_employee:
            return jsonify({"error": "Email already exists"}), 400

        # Update the cache instead of deleting it
        cached_employees = cache.get("employees")

        if cached_employees is not None:
            # Append new employee to the cached list
            cached_employees.append(
                {
                    "id": new_employee.id,
                    "first_name": new_employee.first_name,
                    "last_name": new_employee.last_name,
                    "email": new_employee.email,
                }
            )
            # Update cacheing
            cache.set("employees", cached_employees, timeout=600)

        return (
            jsonify(
                {
                    "id": new_employee.id,
                    "first_name": new_employee.first_name,
                    "last_name": new_employee.last_name,
                    "email": new_employee.email,
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": "An error occurred", "message": str(e)}), 500
