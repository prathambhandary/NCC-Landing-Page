from flask import request, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies
from config import Config

def login():

    data = request.get_json()

    print(data)

    print(Config.ADMIN_USERNAME)
    print(Config.ADMIN_PASSWORD)

    username = data.get("username")
    password = data.get("password")

    if (
        username != Config.ADMIN_USERNAME or 
        password != Config.ADMIN_PASSWORD
    ):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity="admin")

    response = jsonify({
        "success": True
    })

    set_access_cookies(response, token)

    return response