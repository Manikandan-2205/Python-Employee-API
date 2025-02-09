from flask import Blueprint, request, jsonify
from flasgger import swag_from
from models.employee import Employee
from flask_jwt_extended import jwt_required
from manager.db import db

emp_bp = Blueprint("employee", __name__)


@emp_bp.route("/", methods=["GET"])
@jwt_required()  # Protect this route
@swag_from(
    {
        "tags": ["Employees"],
        "summary": "Get all employees (Requires JWT token)",
        "description": "This endpoint requires a valid JWT token to access.",
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
            },
            401: {"description": "Unauthorized access"},
        },
        "security": [{"Bearer": []}],
    }
)
def get_employees():
    """Get all employees
    ---
    tags:
      - Employees
    """
    try:
        employees = Employee.get_all()
        employees_list = [
            {
                "id": emp.id,
                "first_name": emp.first_name,
                "last_name": emp.last_name,
                "email": emp.email,
            }
            for emp in employees
        ]
        return jsonify(success=True, data=employees_list), 200
    except Exception as e:
        return (
            jsonify(
                {
                    "error": "An error occurred while fetching employees",
                    "message": str(e),
                }
            ),
            500,
        )


@emp_bp.route("/<int:emp_id>", methods=["GET"])
@jwt_required()  # Protect this route
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
            401: {"description": "Unauthorized access"},
        },
        "security": [{"Bearer": []}],
    }
)
def get_employee_by_id(emp_id):
    """Get an employee by ID
    ---
    tags:
      - Employees
    """
    try:
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
    except Exception as e:
        return (
            jsonify(
                {
                    "error": "An error occurred while fetching the employee",
                    "message": str(e),
                }
            ),
            500,
        )


@emp_bp.route("/", methods=["POST"])
@jwt_required()  # Protect this route
@swag_from(
    {
        "tags": ["Employees"],
        "summary": "Create a new employee (Requires JWT token)",
        "description": "This endpoint requires a valid JWT token to create an employee.",
        "parameters": [
            {
                "name": "employee",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "email": {"type": "string"},
                    },
                },
            }
        ],
        "responses": {
            201: {"description": "Employee created successfully"},
            400: {"description": "Invalid input"},
            401: {"description": "Unauthorized access"},
        },
        "security": [{"Bearer": []}],
    }
)
def create_employee():
    """Create a new employee
    ---
    tags:
      - Employees
    """
    data = request.get_json()
    if not data or not all(key in data for key in ("first_name", "last_name", "email")):
        return jsonify({"error": "Invalid input"}), 400

    try:
        new_employee = Employee.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
        )
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
        return (
            jsonify(
                {
                    "error": "An error occurred while creating the employee",
                    "message": str(e),
                }
            ),
            500,
        )
