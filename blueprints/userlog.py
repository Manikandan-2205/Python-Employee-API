# blueprints/userlog.py
from flask import Blueprint, jsonify

log_bp = Blueprint("log", __name__)

@log_bp.route("/logs", methods=["POST"])
def create_log():    
    return jsonify({"message": "Log created"}), 201