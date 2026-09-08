import random
import string
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.models import Captcha
from app.config.config import EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_FROM
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 生成验证码
def generate_captcha(length: int = 6) -> str:
    # 仅使用大写字母
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(length))

# 存储验证码
def store_captcha(db: Session, email: str, captcha: str, expire_minutes: int = 5):
    # 先删除该邮箱的旧验证码
    db.query(Captcha).filter(Captcha.email == email).delete()
    
    # 修复时区问题，使用utcnow()替代
    # 计算过期时间
    expires_at = datetime.utcnow() + timedelta(minutes=expire_minutes)
    
    # 创建新的验证码记录
    db_captcha = Captcha(
        email=email,
        captcha=captcha,
        expires_at=expires_at
    )
    
    db.add(db_captcha)
    db.commit()
    db.refresh(db_captcha)
    return db_captcha

# 验证验证码
def verify_captcha(db: Session, email: str, captcha: str) -> bool:
    # 查询数据库中的验证码
    db_captcha = db.query(Captcha).filter(Captcha.email == email).first()
    
    # 检查验证码是否存在
    if not db_captcha:
        return False
    
    # 修复时区问题，使用utcnow()替代
    # 检查验证码是否过期
    if datetime.utcnow() > db_captcha.expires_at:
        # 过期则删除
        db.delete(db_captcha)
        db.commit()
        return False
    
    # 检查验证码是否匹配
    if db_captcha.captcha != captcha:
        return False
    
    # 验证成功后删除验证码（可选）
    db.delete(db_captcha)
    db.commit()
    
    return True

# 发送验证码邮件
def send_verification_email(to_email: str, captcha: str):
    subject = "您的注册验证码"
    body = f"尊敬的用户，\n\n您的注册验证码是：{captcha}\n\n该验证码将在5分钟后过期，请及时使用。\n\n请勿将验证码泄露给他人。\n\n感谢您的注册！"
    
    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # 添加邮件正文
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        # 添加详细的调试信息
        print(f"尝试连接到邮件服务器: {EMAIL_HOST}:{EMAIL_PORT}")
        print(f"使用账户: {EMAIL_USERNAME}")
        
        # 连接到SMTP服务器
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.set_debuglevel(1)  # 启用调试模式，显示详细的SMTP交互
        server.starttls()  # 启用TLS加密
        
        print("TLS加密已启用，尝试登录...")
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)  # 登录邮件账户
        
        # 发送邮件
        text = msg.as_string()
        print("登录成功，尝试发送邮件...")
        server.sendmail(EMAIL_FROM, to_email, text)
        server.quit()
        
        print("邮件发送成功")
        return True
    except Exception as e:
        print(f"发送邮件失败: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        # 尝试获取更详细的错误信息
        import traceback
        traceback.print_exc()
        return False