from flask import Blueprint, request, jsonify
from services.auth_service import authenticate

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return ("", 204)
    
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    token = authenticate(username, password)
    if not token:
        return jsonify({"error": "Invalid credentials"}), 401
    
    return jsonify({"token": token})
