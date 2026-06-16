from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import sys

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "admin")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "typhoon_system")

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"

DB_AVAILABLE = False
engine = None
SessionLocal = None
Base = declarative_base()

try:
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        pool_recycle=3600
    )
    # 测试连接
    with engine.connect() as conn:
        conn.execute("SELECT 1")
    SessionLocal = sessionmaker(bind=engine)
    DB_AVAILABLE = True
    print("[DB] MySQL 连接成功", file=sys.stderr)
except Exception as e:
    print(f"[DB] MySQL 不可用，使用无数据库模式: {e}", file=sys.stderr)
    engine = None
    SessionLocal = None
    DB_AVAILABLE = False
