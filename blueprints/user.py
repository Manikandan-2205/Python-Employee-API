# blueprints/user.py
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from flask_jwt_extended import jwt_required
from models.user import User

user_bp = Blueprint("user", __name__)

@user_bp.route("/", methods=["POST"])
@jwt_required()
@swag_from(
    {
        "tags": ["Users"],
        "summary": "Create a new user",
        "description": "Creates a new user in the system.",
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string"},
                        "password": {"type": "string"},
                        "role": {"type": "string"},
                    },
                    "required": ["username", "password", "role"],
                },
            }
        ],
        "responses": {
            201: {
                "description": "User  created successfully",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "username": {"type": "string"},
                    },
                },
            },
            400: {
                "description": "Invalid input or username already exists",
                "schema": {
                    "type": "object",
                    "properties": {"error": {"type": "string"}},
                },
            },
        },
    }
)
def create_user():
    """Create a new user"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    try:
        new_user = User.create(username, password, role)
        return jsonify({"id": new_user.id, "username": new_user.username}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
@swag_from(
    {
        "tags": ["Users"],
        "parameters": [
            {
                "name": "user_id",
                "in": "path",
                "type": "integer",
                "required": True,
                "description": "User  ID",
            }
        ],
        "responses": {
            200: {
                "description": "User  details",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "username": {"type": "string"},
                        "role": {"type": "string"},
                    },
                },
            },
            404: {"description": "User  not found"},
        },
    }
)
def get_user_by_id(user_id):
    """Get a user by ID"""
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({"error": "User  not found"}), 404

    return (
        jsonify(
            {
                "id": user.id,
                "username": user.username,
                "role": user.role,
            }
        ),
        200,
    )

@user_bp.route("/", methods=["GET"])
@jwt_required()
@swag_from(
    {
        "tags": ["Users"],
        "responses": {
            200: {
                "description": "List of users",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "username": {"type": "string"},
                            "role": {"type": "string"},
                        },
                    },
                },
            },
        },
    }
)
def get_all_users():
    """Get all users"""
    users = User.get_all()
    users_list = [
        {
            "id": user.id,
            "username": user.username,
            "role": user.role,
        }
        for user in users
    ]
    return jsonify(users_list), 200