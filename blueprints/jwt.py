from flask import Blueprint, request, jsonify, current_app
from flasgger import swag_from
from flask_jwt_extended import create_access_token, jwt_required
from manager.db import db
from models.jwt import JWTToken
from models.user import User
from models.userlog import UserLog
import bcrypt
import jwt
from datetime import datetime, timedelta


jwt_bp = Blueprint("jwt", __name__)


# @jwt_bp.route("/login", methods=["POST"])
# @swag_from(
#     {
#         "tags": ["Authentication"],
#         "summary": "User   Login",
#         "description": "Logs in a user and returns a JWT token.",
#         "parameters": [
#             {
#                 "name": "body",
#                 "in": "body",
#                 "required": True,
#                 "schema": {
#                     "type": "object",
#                     "properties": {
#                         "username": {"type": "string"},
#                         "password": {"type": "string"},
#                     },
#                     "required": ["username", "password"],
#                 },
#             }
#         ],
#         "responses": {
#             200: {
#                 "description": "JWT token created successfully",
#                 "schema": {
#                     "type": "object",
#                     "properties": {
#                         "token": {"type": "string", "example": "your_jwt_token"}
#                     },
#                 },
#             },
#             401: {"description": "Invalid username or password"},
#         },
#     }
# )
# def login():
#     """User  login route to generate or return existing JWT token."""
#     try:
#         data = request.get_json()
#         username = data.get("username")
#         password = data.get("password")

#         user = User.query.filter_by(username=username).first()
#         if user and bcrypt.checkpw(
#             password.encode("utf-8"), user.password.encode("utf-8")
#         ):
#             existing_token = (
#                 JWTToken.query.filter_by(user_id=user.id)
#                 .order_by(JWTToken.createdtime.desc())
#                 .first()
#             )

#             if existing_token:
#                 try:
#                     decoded_token = jwt.decode(
#                         existing_token.token,
#                         current_app.config["JWT_SECRET_KEY"],
#                         algorithms=["HS256"],
#                     )

#                     if decoded_token["exp"] > datetime.utcnow().timestamp():
#                         # Log the user login
#                         log_user_login(user.id)
#                         return jsonify({"token": existing_token.token}), 200
#                 except jwt.ExpiredSignatureError:
#                     pass
#                 except jwt.InvalidTokenError:
#                     pass

#             # If no valid token exists, create a new one
#             expires = timedelta(hours=1)
#             token = create_access_token(identity=str(user.id), expires_delta=expires)

#             # Store the new token in the database
#             jwt_token = JWTToken.create(token=token, user_id=user.id)

#             # Log the user login
#             log_user_login(user.id)


#             return jsonify({"token": token}), 200
#         else:
#             return jsonify({"error": "Invalid username or password"}), 401
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @jwt_bp.route("/login", methods=["POST"])
# @swag_from(
#     {
#         "tags": ["Authentication"],
#         "summary": "User   Login",
#         "description": "Logs in a user and returns a JWT token.",
#         "parameters": [
#             {
#                 "name": "body",
#                 "in": "body",
#                 "required": True,
#                 "schema": {
#                     "type": "object",
#                     "properties": {
#                         "username": {"type": "string"},
#                         "password": {"type": "string"},
#                     },
#                     "required": ["username", "password"],
#                 },
#             }
#         ],
#         "responses": {
#             200: {
#                 "description": "JWT token created successfully",
#                 "schema": {
#                     "type": "object",
#                     "properties": {
#                         "token": {"type": "string", "example": "your_jwt_token"}
#                     },
#                 },
#             },
#             401: {"description": "Invalid username or password"},
#         },
#     }
# )
# def login():
#     """User   login route to generate or return existing JWT token."""
#     try:
#         data = request.get_json()
#         username = data.get("username")
#         password = data.get("password")

#         if not username or not password:
#             return jsonify({"error": "Username and password are required."}), 400

#         user = User.query.filter_by(username=username).first()
#         if user and bcrypt.checkpw(
#             password.encode("utf-8"), user.password.encode("utf-8")
#         ):
#             existing_token = (
#                 JWTToken.query.filter_by(user_id=user.id)
#                 .order_by(JWTToken.createdtime.desc())
#                 .first()
#             )

#             if existing_token:
#                 try:
#                     decoded_token = jwt.decode(
#                         existing_token.token,
#                         current_app.config["JWT_SECRET_KEY"],
#                         algorithms=["HS256"],
#                     )

#                     if decoded_token["exp"] > datetime.utcnow().timestamp():
#                         UserLog.create_log(user.id)  # Log the user login
#                         return jsonify({"token": existing_token.token}), 200
#                 except jwt.ExpiredSignatureError:
#                     pass
#                 except jwt.InvalidTokenError:
#                     pass

#             # If no valid token exists, create a new one
#             expires = timedelta(hours=1)
#             token = create_access_token(identity=str(user.id), expires_delta=expires)

#             # Store the new token in the database
#             jwt_token = JWTToken.create(token=token, user_id=user.id)

#             # Log the user login directly in the UserLog table
#             UserLog.create_log(user.id)


#             return jsonify({"token": token}), 200
#         else:
#             return jsonify({"error": "Invalid username or password"}), 401
#     except Exception as e:
#         # Log the error for debugging
#         print(f"Login error: {str(e)}")  # Print the error to the console
#         return (
#             jsonify({"error": "An internal server error occurred.", "details": str(e)}),
#             500,
#         )


@jwt_bp.route("/login", methods=["POST"])
@swag_from(
    {
        "tags": ["Authentication"],
        "summary": "User  Login",
        "description": "Logs in a user and returns a JWT token.",
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
                    },
                    "required": ["username", "password"],
                },
            }
        ],
        "responses": {
            200: {
                "description": "JWT token created successfully",
                "schema": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string", "example": "your_jwt_token"}
                    },
                },
            },
            401: {"description": "Invalid username or password"},
        },
    }
)
def login():
    """User  login route to generate or return existing JWT token."""
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required."}), 400

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(
            password.encode("utf-8"), user.password.encode("utf-8")
        ):
            existing_token = (
                JWTToken.query.filter_by(user_id=user.id)
                .order_by(JWTToken.createdtime.desc())
                .first()
            )

            if existing_token:
                try:
                    decoded_token = jwt.decode(
                        existing_token.token,
                        current_app.config["JWT_SECRET_KEY"],
                        algorithms=["HS256"],
                    )

                    if decoded_token["exp"] > datetime.now().timestamp():
                        UserLog.create_log(user.id)
                        return jsonify({"token": existing_token.token}), 200
                except jwt.ExpiredSignatureError:
                    pass
                except jwt.InvalidTokenError:
                    pass

            expires = timedelta(hours=1)
            token = create_access_token(identity=str(user.id), expires_delta=expires)

            jwt_token = JWTToken.create(token=token, user_id=user.id)

            UserLog.create_log(user.id)

            return jsonify({"token": token}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    except Exception as e:
        return (
            jsonify({"error": "An internal server error occurred.", "details": str(e)}),
            500,
        )


@jwt_bp.route("/protected", methods=["GET"])
@jwt_required()
@swag_from(
    {
        "tags": ["Authentication"],
        "summary": "Protected Route",
        "description": "This route requires a valid JWT token.",
        "responses": {
            200: {
                "description": "Access granted",
                "schema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "example": "This is a protected route.",
                        }
                    },
                },
            },
            401: {"description": "Token is missing or invalid"},
        },
    }
)
def protected():
    """A protected route that requires a valid JWT token."""
    return jsonify({"message": "This is a protected route."}), 200
