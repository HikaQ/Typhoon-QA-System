from flask import Blueprint, g, jsonify, request

from utils.auth_utils import create_access_token, login_required
from utils.db import SessionLocal, DB_AVAILABLE
from utils.models import Admin, User
from utils.logging import record_log
from utils.security_utils import hash_password, verify_password

bp = Blueprint("user", __name__, url_prefix="/user")

# 临时固定账号 — MySQL 不可用时使用
FIXED_USERS = {
    "user": {"id": 1, "username": "user", "password": "123456", "type": "user"},
    "admin": {"id": 1, "username": "admin", "password": "123456", "type": "admin", "role": "super_admin"},
}


def _fixed_login(username: str, password: str, required_type: str):
    """固定账号登录，返回 (payload_dict, error_msg)"""
    account = FIXED_USERS.get(username)
    if not account:
        return None, f"{'管理员' if required_type == 'admin' else '用户'}账号不存在"
    if account["type"] != required_type:
        return None, f"{'管理员' if required_type == 'admin' else '用户'}账号不存在"
    if account["password"] != password:
        return None, "密码错误"
    return account, None


@bp.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"msg": "用户名和密码不能为空"}), 400

    # === 无 MySQL 模式：固定账号 ===
    if not DB_AVAILABLE:
        account, err = _fixed_login(username, password, "user")
        if err:
            return jsonify({"msg": err}), 401
        token = create_access_token(account["id"], account["type"], account["username"])
        return jsonify({
            "msg": "登录成功（离线模式）",
            "token": token,
            "user": {
                "id": account["id"],
                "username": account["username"],
                "email": "",
                "real_name": "",
                "type": account["type"],
            },
        }), 200

    # === MySQL 模式 ===
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            ip = request.headers.get("X-Forwarded-For", request.remote_addr)
            record_log(0, username, "login", module="user", ip_address=ip, status="failure")
            return jsonify({"msg": "用户不存在"}), 401
        if not user.is_active:
            ip = request.headers.get("X-Forwarded-For", request.remote_addr)
            record_log(user.id if user else 0, username, "login_disabled", module="user", ip_address=ip, status="failure")
            return jsonify({"msg": "账号已被禁用"}), 403
        if not verify_password(password, user.password_hash):
            ip = request.headers.get("X-Forwarded-For", request.remote_addr)
            record_log(user.id if user else 0, username, "login", module="user", ip_address=ip, status="failure")
            return jsonify({"msg": "密码错误"}), 401

        token = create_access_token(user.id, "user", user.username)
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        record_log(user.id, user.username, "login", module="user", ip_address=ip, status="success")
        return jsonify(
            {
                "msg": "登录成功",
                "token": token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "real_name": user.real_name,
                    "type": "user",
                },
            }
        ), 200
    finally:
        db.close()


@bp.route("/admin-login", methods=["POST"])
def admin_login():
    data = request.json or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"msg": "用户名和密码不能为空"}), 400

    # === 无 MySQL 模式：固定账号 ===
    if not DB_AVAILABLE:
        account, err = _fixed_login(username, password, "admin")
        if err:
            return jsonify({"msg": err}), 401
        token = create_access_token(account["id"], account["type"], account["username"], role=account.get("role"))
        return jsonify({
            "msg": "登录成功（离线模式）",
            "token": token,
            "user": {
                "id": account["id"],
                "username": account["username"],
                "email": "",
                "real_name": "",
                "role": account.get("role", ""),
                "type": account["type"],
            },
        }), 200

    # === MySQL 模式 ===
    db = SessionLocal()
    try:
        admin = db.query(Admin).filter(Admin.username == username).first()
        if not admin:
            ip = request.headers.get("X-Forwarded-For", request.remote_addr)
            record_log(0, username, "admin_login", module="user", ip_address=ip, status="failure")
            return jsonify({"msg": "管理员账号不存在"}), 401
        if not admin.is_active:
            ip = request.headers.get("X-Forwarded-For", request.remote_addr)
            record_log(admin.id if admin else 0, username, "admin_login_disabled", module="user", ip_address=ip, status="failure")
            return jsonify({"msg": "账号已被禁用"}), 403
        if not verify_password(password, admin.password_hash):
            ip = request.headers.get("X-Forwarded-For", request.remote_addr)
            record_log(admin.id if admin else 0, username, "admin_login", module="user", ip_address=ip, status="failure")
            return jsonify({"msg": "密码错误"}), 401

        token = create_access_token(admin.id, "admin", admin.username, role=admin.role)
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        record_log(admin.id, admin.username, "admin_login", module="user", ip_address=ip, status="success")
        return jsonify(
            {
                "msg": "登录成功",
                "token": token,
                "user": {
                    "id": admin.id,
                    "username": admin.username,
                    "email": admin.email,
                    "real_name": admin.real_name,
                    "role": admin.role,
                    "type": "admin",
                },
            }
        ), 200
    finally:
        db.close()


@bp.route("/register", methods=["POST"])
def register():
    if not DB_AVAILABLE:
        return jsonify({"msg": "离线模式下暂不支持注册"}), 503

    data = request.json or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    email = (data.get("email") or "").strip() or None

    if not username or not password:
        return jsonify({"msg": "用户名和密码不能为空"}), 400

    db = SessionLocal()
    try:
        if db.query(User).filter(User.username == username).first():
            ip = request.headers.get("X-Forwarded-For", request.remote_addr)
            record_log(0, username, "register", module="user", ip_address=ip, status="failure")
            return jsonify({"msg": "用户名已存在"}), 400
        if email and db.query(User).filter(User.email == email).first():
            return jsonify({"msg": "邮箱已被使用"}), 400

        user = User(
            username=username,
            password_hash=hash_password(password),
            email=email,
            user_type="user",
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_access_token(user.id, "user", user.username)
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        record_log(user.id, user.username, "register", module="user", ip_address=ip, status="success")
        return jsonify(
            {
                "msg": "注册成功",
                "token": token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "real_name": user.real_name,
                    "type": "user",
                },
            }
        ), 201
    except Exception as e:
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        record_log(0, username, "register", module="user", ip_address=ip, status="failure")
        db.rollback()
        return jsonify({"msg": f"注册失败: {str(e)}"}), 400
    finally:
        db.close()


@bp.route("/profile/<int:user_id>", methods=["GET"])
@login_required()
def get_profile(user_id):
    current_user = g.current_user
    if current_user.get("type") == "user" and int(current_user.get("id")) != user_id:
        return jsonify({"msg": "无权访问其他用户资料"}), 403

    if not DB_AVAILABLE:
        return jsonify({
            "id": current_user.get("id"),
            "username": current_user.get("username"),
            "email": "",
            "phone": "",
            "real_name": "",
            "bio": "",
            "avatar": "",
            "created_at": "",
        }), 200

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"msg": "用户不存在"}), 404

        return jsonify(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "real_name": user.real_name,
                "bio": user.bio,
                "avatar": user.avatar,
                "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S") if user.created_at else None,
            }
        ), 200
    finally:
        db.close()


@bp.route("/profile/<int:user_id>", methods=["PUT"])
@login_required()
def update_profile(user_id):
    current_user = g.current_user
    if current_user.get("type") == "user" and int(current_user.get("id")) != user_id:
        return jsonify({"msg": "无权修改其他用户资料"}), 403

    if not DB_AVAILABLE:
        return jsonify({"msg": "离线模式下暂不支持修改资料"}), 503

    data = request.json or {}
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"msg": "用户不存在"}), 404

        if "email" in data:
            email = (data["email"] or "").strip() or None
            existing_email = db.query(User).filter(User.email == email, User.id != user_id).first()
            if existing_email:
                return jsonify({"msg": "该邮箱已被使用"}), 400
            user.email = email

        if "phone" in data:
            user.phone = data["phone"]
        if "real_name" in data:
            user.real_name = data["real_name"]
        if "bio" in data:
            user.bio = data["bio"]
        if "avatar" in data:
            user.avatar = data["avatar"]

        db.commit()
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        record_log(current_user.get("id"), current_user.get("username"), "update_profile", module="user", ip_address=ip, status="success")
        return jsonify({"msg": "用户信息更新成功"}), 200
    except Exception as e:
        db.rollback()
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        record_log(current_user.get("id"), current_user.get("username"), "update_profile", module="user", ip_address=ip, status="failure")
        return jsonify({"msg": f"更新失败: {str(e)}"}), 400
    finally:
        db.close()


@bp.route("/admin/<int:admin_id>", methods=["GET"])
@login_required("admin")
def get_admin(admin_id):
    if not DB_AVAILABLE:
        current_user = g.current_user
        return jsonify({
            "id": current_user.get("id"),
            "username": current_user.get("username"),
            "email": "",
            "phone": "",
            "real_name": "",
            "role": current_user.get("role", "admin"),
            "created_at": "",
        }), 200

    db = SessionLocal()
    try:
        admin = db.query(Admin).filter(Admin.id == admin_id).first()
        if not admin:
            return jsonify({"msg": "管理员不存在"}), 404

        return jsonify(
            {
                "id": admin.id,
                "username": admin.username,
                "email": admin.email,
                "phone": admin.phone,
                "real_name": admin.real_name,
                "role": admin.role,
                "created_at": admin.created_at.strftime("%Y-%m-%d %H:%M:%S") if admin.created_at else None,
            }
        ), 200
    finally:
        db.close()


@bp.route("/admin/<int:admin_id>", methods=["PUT"])
@login_required("admin")
def update_admin(admin_id):
    if not DB_AVAILABLE:
        return jsonify({"msg": "离线模式下暂不支持修改管理员信息"}), 503

    data = request.json or {}
    db = SessionLocal()
    try:
        admin = db.query(Admin).filter(Admin.id == admin_id).first()
        if not admin:
            return jsonify({"msg": "管理员不存在"}), 404

        if "email" in data:
            email = (data["email"] or "").strip() or None
            existing_email = db.query(Admin).filter(Admin.email == email, Admin.id != admin_id).first()
            if existing_email:
                return jsonify({"msg": "该邮箱已被使用"}), 400
            admin.email = email

        if "phone" in data:
            admin.phone = data["phone"]
        if "real_name" in data:
            admin.real_name = data["real_name"]
        if "role" in data:
            admin.role = data["role"]

        db.commit()
        return jsonify({"msg": "管理员信息更新成功"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"msg": f"更新失败: {str(e)}"}), 400
    finally:
        db.close()
