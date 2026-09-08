from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 验证密码
def verify_password(plain_password, stored_password):
    # 直接比较明文密码（注意：这在生产环境中非常不安全！）
    return plain_password == stored_password

# 获取密码哈希
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 创建访问令牌
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 模拟用户数据库（用于测试）
fake_users_db = {
    "admin": {
        "userId": 1,
        "username": "admin",
        "password": pwd_context.hash("admin123")
    },
    "user": {
        "userId": 2,
        "username": "user",
        "password": pwd_context.hash("user123")
    }
}

# 获取用户
def get_user(db, username: str):
    if username in db:
        return db[username]
    return None