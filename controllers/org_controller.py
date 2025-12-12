from flask import Blueprint, request, jsonify, g
from services.org_service import create_org, get_org_by_name, update_org, delete_org
from middleware.auth_middleware import auth_required

org_bp = Blueprint("org", __name__, url_prefix="/org")

@org_bp.post("/create")
def create():
    data = request.get_json(force=True, silent=True) or {}
    name = data.get("organization_name")
    email = data.get("email")
    password = data.get("password")
    if not name or not email or not password:
        return jsonify({"error": "organization_name, email, and password are required"}), 400
    code, payload = create_org(name, email, password)
    return jsonify(payload), code

@org_bp.get("/get")
def get():
    name = request.args.get("organization_name")
    if not name:
        data = request.get_json(silent=True) or {}
        name = data.get("organization_name")
    if not name:
        return jsonify({"error": "organization_name is required"}), 400
    code, payload = get_org_by_name(name)
    return jsonify(payload), code

@org_bp.put("/update")
def update():
    data = request.get_json(force=True, silent=True) or {}
    new_name = data.get("organization_name")
    email = data.get("email")
    password = data.get("password")
    if not new_name or not email or not password:
        return jsonify({"error": "organization_name, email, and password are required"}), 400
    code, payload = update_org(new_name, email, password)
    return jsonify(payload), code

@org_bp.delete("/delete")
@auth_required
def delete():
    data = request.get_json(force=True, silent=True) or {}
    name = data.get("organization_name")
    if not name:
        return jsonify({"error": "organization_name is required"}), 400
    code, payload = delete_org(name, getattr(g, "claims", None))
    return jsonify(payload), code

