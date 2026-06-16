from flask import Blueprint, request, jsonify
from utils.db import SessionLocal, DB_AVAILABLE
from utils.models import Log

bp = Blueprint("log", __name__, url_prefix="/log")


@bp.route("", methods=["GET"])
def list_logs():
    if not DB_AVAILABLE:
        return jsonify({"total": 0, "logs": [], "msg": "离线模式，日志不可用"}), 200

    try:
        limit = int(request.args.get("limit", 100))
    except ValueError:
        limit = 100
    try:
        offset = int(request.args.get("offset", 0))
    except ValueError:
        offset = 0

    status = request.args.get("status")
    module = request.args.get("module")
    username = request.args.get("username")

    db = SessionLocal()
    try:
        query = db.query(Log)
        if status:
            query = query.filter(Log.status == status)
        if module:
            query = query.filter(Log.module == module)
        if username:
            query = query.filter(Log.username == username)

        total = query.count()
        rows = query.order_by(Log.create_time.desc()).offset(offset).limit(limit).all()

        ACTION_BASE = {
            "admin_login": "管理员登录",
            "login": "用户登录",
            "register": "用户注册",
            "update_profile": "更新用户资料",
            "login_disabled": "禁用账号登录尝试",
            "admin_login_disabled": "禁用管理员登录尝试",
        }

        def human_action_label(action, status):
            base = ACTION_BASE.get(action)
            if not base:
                base = (action or "").replace("_", " ")
            if not status:
                return base
            s = str(status).lower()
            if s in ("success", "info"):
                return f"{base} 成功"
            if s in ("failure", "error"):
                return f"{base} 失败"
            if s == "warning":
                return f"{base} 警告"
            return f"{base} ({status})"

        def to_dict(r):
            return {
                "id": r.id,
                "user_id": r.user_id,
                "username": r.username,
                "action": r.action,
                "action_label": human_action_label(r.action, r.status),
                "module": r.module,
                "ip_address": r.ip_address,
                "status": r.status,
                "create_time": r.create_time.strftime("%Y-%m-%d %H:%M:%S") if r.create_time else None,
            }

        return jsonify({"total": total, "logs": [to_dict(r) for r in rows]}), 200
    except Exception as e:
        return jsonify({"msg": f"查询日志失败: {str(e)}"}), 500
    finally:
        db.close()


@bp.route("", methods=["DELETE"])
def clear_logs():
    if not DB_AVAILABLE:
        return jsonify({"msg": "离线模式，日志不可用"}), 503

    db = SessionLocal()
    try:
        deleted = db.query(Log).delete()
        db.commit()
        return jsonify({"msg": "已清空日志", "deleted": deleted}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"msg": f"清空日志失败: {str(e)}"}), 500
    finally:
        db.close()
