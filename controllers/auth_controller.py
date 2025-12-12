from flask import Blueprint, request, jsonify
from services.auth_service import admin_login

auth_bp = Blueprint("auth", __name__, url_prefix="/admin")

@auth_bp.post("/login")
def login():
    data = request.get_json(force=True, silent=True) or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400
    code, payload = admin_login(email, password)
    return jsonify(payload), code

