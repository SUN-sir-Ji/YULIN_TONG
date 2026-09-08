from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.core.database import Base, engine
import uvicorn

# 创建FastAPI应用（只创建一次）
app = FastAPI(title="Plant Recognition System API", description="植物识别系统后端API", version="1.0.0")

# 添加CORS中间件，允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应设置为具体的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含所有路由
app.include_router(api_router)

# 根路由
@app.get("/")
def read_root():
    return {"message": "欢迎使用植物识别系统API"}

# ============== 应用启动配置 ==============
# 创建所有数据库表
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# 启动应用（用于开发环境）
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)