from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.config import DATABASE_URL

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    pool_size=10,            # 连接池大小
    max_overflow=20,         # 最大溢出连接数
    pool_timeout=30,         # 获取连接的超时时间（秒）
    pool_recycle=1800,       # 连接回收时间（秒），建议小于MySQL wait_timeout（默认28800秒）
    pool_pre_ping=True       # 每次从池中获取连接前验证连接是否有效
)

# 创建SessionLocal类，每个实例都是一个数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建Base类，后续所有模型都将继承此类
Base = declarative_base()

# 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()