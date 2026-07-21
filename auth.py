from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    verify_jwt_in_request,
    get_jwt_identity
)
from config import Config

def login():
    data = request.get_json()
    password = data.get("password")

    if password != Config.ADMIN_PASSWORD:
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity="admin")
    response = jsonify({"success": True})
    set_access_cookies(response, token)
    return response

def verify():
    """Check if the JWT cookie is valid and belongs to admin."""
    try:
        verify_jwt_in_request(locations=["cookies"])
        identity = get_jwt_identity()
        if identity == "admin":
            return jsonify({"valid": True})
        return jsonify({"valid": False}), 401
    except Exception:
        return jsonify({"valid": False}), 401

def logout():
    """Clear the JWT cookie."""
    response = jsonify({"success": True})
    unset_jwt_cookies(response)
    return response