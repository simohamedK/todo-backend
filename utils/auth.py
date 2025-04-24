import jwt
from flask import request, jsonify, current_app
from functools import wraps
from datetime import datetime, timedelta, timezone
from config import SECRET_KEY

class JWTManager:

    @staticmethod
    def generate_token(payload, expires_in=60):
        payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=expires_in)
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def verify_jwt(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def token_required(f):
        @wraps(f) # Garde le nom et les infos originales de la fonction décorée
        def decorated(*args, **kwargs):
            token = None

            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token= auth_header.split(" ")[1]  # Extrait le token après "Bearer "
            
            if not token:
                return jsonify({"error": "Token is missing"}), 401
            
            payload =  JWTManager.verify_jwt(token)
            if not payload:
                return jsonify({"error" : "Token is invalid or expired"}), 401
            
            return f(*args, **kwargs, user_id=payload["id"])
        return decorated

    def admin_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

            if not token:
                return jsonify({"error": "Token is missing"}), 401

            payload = JWTManager.verify_jwt(token)
            if not payload:
                return jsonify({"error": "Token is invalid or expired"}), 401

            if payload.get("role") != "admin":
                return jsonify({"error": "Admin access required"}), 403

            return f(*args, **kwargs, user_id=payload["id"])
        return decorated