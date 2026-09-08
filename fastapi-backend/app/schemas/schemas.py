from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any

class LoginRequest(BaseModel):
    username: str
    password: str
    remember: bool = False

class LoginData(BaseModel):
    userId: int
    username: str
    token: str

class LoginResponse(BaseModel):
    code: int
    message: str
    data: LoginData

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    captcha: str

class UserOut(BaseModel):
    user_id: int  # 从str改为int
    email: EmailStr
    
    class Config:
        orm_mode = True

class CaptchaRequest(BaseModel):
    email: EmailStr

class CaptchaResponse(BaseModel):
    message: str
    status: int

class RegisterResponse(BaseModel):
    message: str
    user: Optional[UserOut] = None
    status: int