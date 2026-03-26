from utils.db import engine
from utils.models import Base

Base.metadata.create_all(bind=engine)
print("数据库初始化完成")
