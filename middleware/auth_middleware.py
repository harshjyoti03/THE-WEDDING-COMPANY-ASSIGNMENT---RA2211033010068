from functools import wraps
from flask import request, jsonify, g
from utils.jwt_helper import decode_token

def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "authorization required"}), 401
        token = auth.split(" ", 1)[1]
        claims = decode_token(token)
        if not claims:
            return jsonify({"error": "authorization required"}), 401
        g.claims = claims
        return f(*args, **kwargs)
    return wrapper

