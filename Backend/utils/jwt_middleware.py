from flask import request, jsonify
from services.auth_service import verify_token

def jwt_required(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token missing"}), 401
        
        token = auth_header.split(" ")[1]
        decoded = verify_token(token)
        if not decoded:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  
    return wrapper
