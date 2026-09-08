from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.models import UserInfo
from app.schemas.schemas import UserCreate

# 获取用户通过邮箱
def get_user_by_email(db: Session, email: str):
    return db.query(UserInfo).filter(UserInfo.email == email).first()

# 获取用户通过用户名（user_id）
def get_user_by_username(db: Session, username: str):
    try:
        user_id_int = int(username)
        return db.query(UserInfo).filter(UserInfo.user_id == user_id_int).first()
    except ValueError:
        return None

# 创建用户
def create_user(db: Session, user: UserCreate):
    # 创建用户对象 - 确保user_id是整数类型
    try:
        user_id_int = int(user.username)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名必须是有效的数字，以便作为用户ID"
        )
    
    # 直接使用明文密码（不推荐！）
    db_user = UserInfo(
        user_id=user_id_int,
        email=user.email,
        password=user.password  # 不再进行密码哈希
    )
    
    # 添加到数据库
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user