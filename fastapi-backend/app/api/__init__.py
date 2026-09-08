from fastapi import APIRouter
from app.api import auth_router, plant_router

# 创建主路由
api_router = APIRouter()

# 包含所有子路由
api_router.include_router(auth_router.router)
api_router.include_router(plant_router.router)