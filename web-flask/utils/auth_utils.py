import os
from functools import wraps

from flask import jsonify, g, request
from itsdangerous import BadData, SignatureExpired, URLSafeTimedSerializer


TOKEN_EXPIRES_SECONDS = int(os.getenv("TOKEN_EXPIRES_SECONDS", "86400"))
TOKEN_SECRET_KEY = os.getenv("TOKEN_SECRET_KEY", "typhoon-system-change-me")
TOKEN_SALT = "typhoon-auth-token"


def _serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(TOKEN_SECRET_KEY)


def create_access_token(user_id: int, user_type: str, username: str, role: str | None = None) -> str:
    payload = {
        "id": user_id,
        "type": user_type,
        "username": username,
    }
    if role:
        payload["role"] = role
    return _serializer().dumps(payload, salt=TOKEN_SALT)


def verify_access_token(token: str) -> dict | None:
    try:
        payload = _serializer().loads(token, salt=TOKEN_SALT, max_age=TOKEN_EXPIRES_SECONDS)
    except (SignatureExpired, BadData):
        return None
    return payload


def get_auth_payload() -> dict | None:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header[7:].strip()
    if not token:
        return None
    return verify_access_token(token)


def login_required(required_type: str | None = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            payload = get_auth_payload()
            if not payload:
                return jsonify({"msg": "未登录或登录已过期"}), 401

            if required_type and payload.get("type") != required_type:
                return jsonify({"msg": "权限不足"}), 403

            g.current_user = payload
            return func(*args, **kwargs)

        return wrapper

    return decorator
