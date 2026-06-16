from utils.db import SessionLocal, DB_AVAILABLE
from utils.models import Log
import traceback
import sys


def record_log(user_id, username, action, module=None, ip_address=None, status="success"):
    if not DB_AVAILABLE:
        print(f"[LOG] {username}({user_id}) {action} -> {status}", file=sys.stderr)
        return False

    db = SessionLocal()
    try:
        log = Log(
            user_id=int(user_id) if user_id is not None else 0,
            username=username or "",
            action=action,
            module=module,
            ip_address=ip_address,
            status=status,
        )
        db.add(log)
        db.commit()
        return True
    except Exception as e:
        try:
            db.rollback()
        except Exception:
            pass
        print("[LOGGING] failed to record log:", e, file=sys.stderr)
        traceback.print_exc()
        return False
    finally:
        db.close()


def record_log_with_session(db, user_id, username, action, module=None, ip_address=None, status="success"):
    if not DB_AVAILABLE:
        return None
    log = Log(
        user_id=int(user_id) if user_id is not None else 0,
        username=username or "",
        action=action,
        module=module,
        ip_address=ip_address,
        status=status,
    )
    db.add(log)
    return log
