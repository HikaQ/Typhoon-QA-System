from flask import Blueprint, request, jsonify
from utils.db import SessionLocal
from utils.models import User
from utils.security_utils import hash_password

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg": "用户名和密码不能为空"}), 400

    db = SessionLocal()

    # 是否已存在
    if db.query(User).filter(User.username == username).first():
        return jsonify({"msg": "用户名已存在"}), 400

    user = User(
        username=username,
        password_hash=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.close()

    return jsonify({"msg": "注册成功"})
