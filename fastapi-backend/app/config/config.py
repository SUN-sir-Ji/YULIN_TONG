import os
from dotenv import load_dotenv
from datetime import timedelta

# 加载环境变量
load_dotenv()

# JWT配置
SECRET_KEY = "your-secret-key-here"  # 在生产环境中应使用安全的密钥
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # 如果没有环境变量，使用默认值
    DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/tables"

# 邮件服务器配置
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.qq.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", "3033714509@qq.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "ogiosbnuhziudgig")
EMAIL_FROM = os.getenv("EMAIL_FROM", "3033714509@qq.com")

# 图片存储配置
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")
# 确保上传目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)