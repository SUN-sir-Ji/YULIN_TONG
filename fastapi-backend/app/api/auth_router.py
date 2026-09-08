from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schemas import LoginRequest, LoginResponse, UserCreate, RegisterResponse, CaptchaRequest, CaptchaResponse
from app.services.auth_service import create_access_token, verify_password, get_user, fake_users_db
from app.services.user_service import get_user_by_email, get_user_by_username, create_user
from app.services.captcha_service import generate_captcha, store_captcha, verify_captcha, send_verification_email
from datetime import timedelta
from app.config.config import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/api/auth", tags=["认证"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# 登录接口
@router.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    # 将登录请求中的username转换为整数作为user_id
    try:
        user_id_int = int(login_request.username)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名必须是有效的用户ID数字"
        )
    
    # 从实际数据库中查询用户
    user = get_user_by_username(db, user_id_int)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
        )
    
    # 验证密码
    if not verify_password(login_request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="密码错误",
        )
    
    # 生成JWT令牌
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.user_id)},  # 使用user_id作为主题
        expires_delta=access_token_expires
    )
    
    # 构建响应数据
    response_data = {
        "code": 200,
        "message": "success",
        "data": {
            "userId": user.user_id,
            "username": str(user.user_id),  # 用户名显示为user_id
            "token": access_token
        }
    }
    
    return response_data

# 获取验证码路由
@router.post("/get-captcha", response_model=CaptchaResponse)
async def get_captcha(request: CaptchaRequest = None, email: str = None, db: Session = Depends(get_db)):
    # 优先使用请求体中的邮箱，如果没有则使用查询参数
    target_email = None
    if request:
        target_email = request.email
    elif email:
        target_email = email
    
    if not target_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请提供有效的邮箱地址"
        )
    
    print(f"收到获取验证码请求，邮箱: {target_email}")
    
    # 检查邮箱是否已注册
    existing_user = get_user_by_email(db, target_email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册，请使用其他邮箱"
        )
    
    # 生成验证码
    captcha = generate_captcha()
    print(f"生成验证码: {captcha}")
    
    # 存储验证码
    store_captcha(db, target_email, captcha)
    
    # 发送验证码邮件
    email_sent = send_verification_email(target_email, captcha)
    
    if not email_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="验证码发送失败，请稍后再试"
        )
    
    return {
        "message": "验证码已发送到您的邮箱，请注意查收",
        "status": 200
    }

# 注册路由
@router.post("/register", response_model=RegisterResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    existing_username = get_user_by_username(db, user.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在，请使用其他用户名"
        )
    
    # 检查邮箱是否已注册
    existing_email = get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册，请使用其他邮箱"
        )
    
    # 验证验证码
    captcha_valid = verify_captcha(db, user.email, user.captcha)
    if not captcha_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码不正确或已过期，请重新获取"
        )
    
    # 创建用户
    try:
        db_user = create_user(db, user)
        return {
            "message": "注册成功",
            "user": db_user,
            "status": 201
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"注册失败：{str(e)}"
        )

# 示例：需要认证的接口
@router.get("/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        from jose import jwt
        from app.config.config import SECRET_KEY, ALGORITHM
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    user = get_user(fake_users_db, username=username)
    if user is None:
        raise credentials_exception
    
    return {
        "userId": user["userId"],
        "username": user["username"]
    }

# 忘记密码获取验证码
@router.post("/forgot-password/captcha", response_model=CaptchaResponse)
def get_forgot_password_captcha(request: CaptchaRequest, db: Session = Depends(get_db)):
    # 检查邮箱是否已注册
    existing_user = get_user_by_email(db, request.email)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱未注册"
        )
    
    # 生成验证码
    captcha = generate_captcha()
    
    # 存储验证码
    store_captcha(db, request.email, captcha)
    
    # 发送验证码邮件
    email_sent = send_verification_email(request.email, captcha)
    
    if not email_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="验证码发送失败，请稍后再试"
        )
    
    return {
        "message": "验证码已发送到您的邮箱，请注意查收",
        "status": 200
    }

# 重置密码
@router.post("/reset-password")
def reset_password(request: dict, db: Session = Depends(get_db)):
    email = request.get('email')
    captcha = request.get('captcha')
    
    # 验证验证码
    captcha_valid = verify_captcha(db, email, captcha)
    if not captcha_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码不正确或已过期，请重新获取"
        )
    
    # 查询用户
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 返回密码（注意：这在生产环境中不安全！）
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "password": user.password  # 注意：实际项目中应返回临时密码或重置密码链接
        }
    )