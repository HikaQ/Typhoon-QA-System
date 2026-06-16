from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from utils.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    phone = Column(String(20), nullable=True)
    real_name = Column(String(50), nullable=True)
    bio = Column(String(500), nullable=True)
    avatar = Column(String(500), nullable=True)
    user_type = Column(String(20), default="user", nullable=False)  # user 或 admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, user_type={self.user_type})>"


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    real_name = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    role = Column(String(50), default="admin", nullable=False)  # admin, super_admin 等
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Admin(id={self.id}, username={self.username}, role={self.role})>"


class Log(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String(50), nullable=False)
    action = Column(String(255), nullable=False)
    module = Column(String(50), nullable=True)
    ip_address = Column(String(50), nullable=True)
    status = Column(String(20), nullable=False)
    create_time = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Log(id={self.id}, user_id={self.user_id}, action={self.action}, status={self.status})>"
