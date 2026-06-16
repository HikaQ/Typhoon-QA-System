"""
数据库初始化脚本
运行此脚本创建所有数据库表并添加默认的管理员和用户账号
"""

import os
import sys
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.dirname(__file__))

from utils.db import engine, Base, SessionLocal
from utils.models import User, Admin, Log
from utils.security_utils import hash_password


def create_tables():
    """创建所有数据库表"""
    print("正在创建数据库表...")
    # 先测试数据库连通性
    try:
        conn = engine.connect()
        conn.close()
        print("✓ 数据库连接正常")
    except Exception as e:
        print(f"✗ 无法连接到数据库: {e}")
        return False
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ 数据库表创建成功!")
        return True
    except Exception as e:
        print(f"✗ 创建数据库表失败: {e}")
        return False


def check_tables_exist():
    """检查表是否已存在"""
    inspector = __import__('sqlalchemy').inspect(engine)
    tables = inspector.get_table_names()
    print(f"\n当前数据库中的表: {tables}")
    return tables


def init_admin_user(db):
    """初始化管理员账号"""
    print("\n正在初始化管理员账号...")
    
    # 检查是否已存在管理员
    admin = db.query(Admin).filter(Admin.username == "admin").first()
    if admin:
        print("✓ 管理员账号已存在，跳过初始化")
        return False
    
    # 创建默认管理员
    try:
        admin = Admin(
            username="admin",
            password_hash=hash_password("admin123"),
            email="admin@ts.com",
            real_name="系统管理员",
            phone="1234567890",
            role="super_admin",
            is_active=True
        )
        db.add(admin)
        db.commit()
        print("✓ 管理员账号创建成功!")
        print("  用户名: admin")
        print("  密码: admin123")
        print("  邮箱: admin@ts.com")
        return True
    except Exception as e:
        db.rollback()
        print(f"✗ 创建管理员账号失败: {e}")
        return False


def init_default_user(db):
    """初始化默认测试用户"""
    print("\n正在初始化默认用户...")
    
    # 检查是否已存在测试用户
    user = db.query(User).filter(User.username == "testuser").first()
    if user:
        print("✓ 测试用户已存在，跳过初始化")
        return False
    
    # 创建默认测试用户
    try:
        user = User(
            username="testuser",
            password_hash=hash_password("test123456"),
            email="testuser@ts.com",
            real_name="测试用户",
            phone="1234567890",
            user_type="user",
            is_active=True,
            bio="这是一个测试用户账号"
        )
        db.add(user)
        db.commit()
        print("✓ 测试用户创建成功!")
        print("  用户名: testuser")
        print("  密码: test123456")
        print("  邮箱: testuser@ts.com")
        return True
    except Exception as e:
        db.rollback()
        print(f"✗ 创建测试用户失败: {e}")
        return False


def list_all_users(db):
    """列出所有用户"""
    print("\n" + "="*60)
    print("当前系统中的用户账号:")
    print("="*60)
    
    # 列出管理员
    admins = db.query(Admin).all()
    if admins:
        print("\n【管理员账号】")
        for admin in admins:
            print(f"  用户名: {admin.username}")
            print(f"  角色: {admin.role}")
            print(f"  邮箱: {admin.email}")
            print(f"  真实姓名: {admin.real_name}")
            print(f"  电话: {admin.phone}")
            print(f"  状态: {'激活' if admin.is_active else '禁用'}")
            print(f"  创建时间: {admin.created_at}")
            print()
    
    # 列出用户
    users = db.query(User).all()
    if users:
        print("\n【普通用户账号】")
        for user in users:
            print(f"  用户名: {user.username}")
            print(f"  邮箱: {user.email}")
            print(f"  真实姓名: {user.real_name}")
            print(f"  电话: {user.phone}")
            print(f"  状态: {'激活' if user.is_active else '禁用'}")
            print(f"  创建时间: {user.created_at}")
            print()
    
    if not admins and not users:
        print("当前没有任何账号")
    
    print("="*60 + "\n")


def main():
    """主程序"""
    print("="*60)
    print("台风系统 - 数据库初始化脚本")
    print("="*60)
    
    # 步骤1: 创建表
    if not create_tables():
        print("\n初始化失败!")
        return False
    
    # 步骤2: 检查表
    check_tables_exist()
    
    # 步骤3: 初始化数据
    db = SessionLocal()
    try:
        init_admin_user(db)
        init_default_user(db)
        list_all_users(db)
    finally:
        db.close()
    
    print("\n✓ 数据库初始化完成!")
    print("\n提示:")
    print("1. 请确保MySQL服务正在运行")
    print("2. 默认连接信息:")
    print("   - 主机: localhost")
    print("   - 端口: 3306")
    print("   - 用户: root")
    print("   - 密码: root")
    print("   - 数据库: typhoon_system")
    print("\n3. 如需修改连接信息，请设置环境变量:")
    print("   - MYSQL_HOST")
    print("   - MYSQL_PORT")
    print("   - MYSQL_USER")
    print("   - MYSQL_PASSWORD")
    print("   - MYSQL_DATABASE")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
