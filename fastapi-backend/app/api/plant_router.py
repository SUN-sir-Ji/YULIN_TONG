from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
import os
import uuid
from fastapi.responses import JSONResponse
from app.core.database import get_db
from app.services.plant_service import process_image_recognition
from app.config.config import UPLOAD_DIR

# OAuth2密码承载器
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

router = APIRouter(prefix="/api", tags=["植物"])

# 获取植物列表接口
@router.get("/plants/list")
async def get_plants_list(
    phylum_latin_name: Optional[str] = None,
    class_latin_name: Optional[str] = None,
    order_latin_name: Optional[str] = None,
    family_latin_name: Optional[str] = None,
    genus_latin_name: Optional[str] = None,
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    根据分类层级获取植物列表
    可以根据门、纲、目、科、属的拉丁名进行筛选
    """
    try:
        # 添加详细日志记录
        print("===== 植物列表查询请求 =====")
        print(f"门拉丁名参数: {phylum_latin_name}")
        print(f"纲拉丁名参数: {class_latin_name}")
        print(f"目拉丁名参数: {order_latin_name}")
        print(f"科拉丁名参数: {family_latin_name}")
        print(f"属拉丁名参数: {genus_latin_name}")
        
        # 构建查询
        query = db.query(text("*"))
        
        # 根据传入的参数添加筛选条件
        filters = []
        params = {}
        
        if phylum_latin_name:
            filters.append(text("phylum_latin_name = :phylum_latin_name"))
            params["phylum_latin_name"] = phylum_latin_name
        if class_latin_name:
            filters.append(text("class_latin_name = :class_latin_name"))
            params["class_latin_name"] = class_latin_name
        if order_latin_name:
            filters.append(text("order_latin_name = :order_latin_name"))
            params["order_latin_name"] = order_latin_name
        if family_latin_name:
            filters.append(text("family_latin_name = :family_latin_name"))
            params["family_latin_name"] = family_latin_name
        if genus_latin_name:
            filters.append(text("genus_latin_name = :genus_latin_name"))
            params["genus_latin_name"] = genus_latin_name
        
        print(f"构建的筛选条件: {filters}")
        print(f"绑定的参数: {params}")
        
        # 执行查询
        if filters:
            where_clause = " AND ".join([f"{f}" for f in filters])
            print(f"生成的WHERE子句: {where_clause}")
            # 添加分页参数
            offset = (page - 1) * pageSize
            sql_query = f"SELECT * FROM plant_info WHERE {where_clause} LIMIT {pageSize} OFFSET {offset}"
        else:
            print("没有筛选条件，查询所有植物")
            # 添加分页参数
            offset = (page - 1) * pageSize
            sql_query = f"SELECT * FROM plant_info LIMIT {pageSize} OFFSET {offset}"
        
        print(f"执行的SQL查询: {sql_query}")
        print(f"分页参数 - page: {page}, pageSize: {pageSize}, offset: {offset}")
        # 执行SQL查询
        result = db.execute(text(sql_query), params)
        
        # 获取列名
        columns = result.keys()
        
        # 将结果转换为字典列表
        plants = []
        for row in result:
            plant_dict = dict(zip(columns, row))
            plants.append(plant_dict)
        
        # 记录查询结果
        print(f"查询结果数量: {len(plants)}")
        if plants:
            print("返回的植物数据示例:")
            # 打印第一条记录的部分信息作为示例
            first_plant = plants[0]
            print(f"- 中文名: {first_plant.get('species_chinese_name', '未知')}")
            print(f"- 拉丁名: {first_plant.get('species_latin_name', '未知')}")
            print(f"- 门: {first_plant.get('phylum_latin_name', '未知')}")
            print(f"- 纲: {first_plant.get('class_latin_name', '未知')}")
            print(f"- 目: {first_plant.get('order_latin_name', '未知')}")
            print(f"- 科: {first_plant.get('family_latin_name', '未知')}")
            print(f"- 属: {first_plant.get('genus_latin_name', '未知')}")
        
        # 获取总数用于分页
        count_sql = "SELECT COUNT(*) FROM plant_info"
        if filters:
            count_sql += f" WHERE {where_clause}"
        
        count_result = db.execute(text(count_sql), params)
        total = count_result.scalar()
        
        return {
            "code": 200,
            "message": "success",
            "data": {
                "list": plants,
                "total": total,
                "page": page,
                "pageSize": pageSize
            }
        }
    except Exception as e:
        # 记录错误详情
        print("===== 查询出错 =====")
        print(f"获取植物列表出错: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取植物列表失败: {str(e)}"
        )

# 图片上传接口（临时移除认证要求）
@router.post("/upload/image")
async def upload_image(
    file: UploadFile = File(...)
    # 移除token认证要求: token: str = Depends(oauth2_scheme)
):
    # 移除token验证代码
    # 使用默认用户信息（仅用于开发测试）
    username = "admin"
    user = {
        "userId": 1,
        "username": "admin"
    }
    
    # 生成唯一的文件名
    file_extension = file.filename.split(".")[-1].lower()
    # 使用时间戳和用户ID来确保文件名唯一
    unique_filename = f"{username}_{uuid.uuid4()}.{file_extension}"
    
    # 保存文件到上传目录
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # 调用图片识别函数
    recognition_results = process_image_recognition(file_path)
    
    # 返回响应，包含识别结果
    return JSONResponse(
        status_code=200,
        content={
            "code": 200,
            "message": "success",
            "data": {
                "filename": unique_filename,
                "path": file_path,
                "userId": user["userId"],
                "username": user["username"],
                "recognition_results": recognition_results
            }
        }
    )

# 批量图片上传接口（可选）
@router.post("/upload/images")
async def upload_images(
    files: List[UploadFile] = File(...),
    token: str = Depends(oauth2_scheme)
):
    # 验证用户token（与单张上传相同的验证逻辑）
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
        
        from app.services.auth_service import get_user, fake_users_db
        user = get_user(fake_users_db, username=username)
        if user is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    # 保存所有上传的文件
    uploaded_files = []
    for file in files:
        file_extension = file.filename.split(".")[-1].lower()
        unique_filename = f"{username}_{uuid.uuid4()}.{file_extension}"
        
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        uploaded_files.append({
            "filename": unique_filename,
            "path": file_path
        })
    
    # 调用图片识别函数（使用最后一个文件进行演示）
    recognition_results = []
    if uploaded_files:
        recognition_results = process_image_recognition(uploaded_files[-1]["path"])
    
    # 返回成功响应
    return JSONResponse(
        status_code=200,
        content={
            "code": 200,
            "message": "success",
            "data": {
                "files": uploaded_files,
                "userId": user["userId"],
                "username": user["username"],
                "recognition_results": recognition_results
            }
        }
    )

# 获取植物分类
@router.get("/plants/categories")
async def get_plant_categories(parent_id: int = 0, db: Session = Depends(get_db)):
    try:
        # 简单的查询，直接使用plant_id的层级关系
        if parent_id == 0:
            # 查询一级分类(plant_id为单个数字)
            query = text("""
                SELECT c.id, c.plant_name as name, c.plant_value as value,
                       (SELECT COUNT(*) FROM plant_category WHERE plant_id LIKE CONCAT(c.plant_id, '.%')) > 0 as hasChildren
                FROM plant_category c
                WHERE c.plant_id REGEXP '^[0-9]+$'
                ORDER BY c.plant_id
            """)
            result = db.execute(query).fetchall()
        else:
            # 根据parent_id查询下一级分类
            parent_query = text("SELECT plant_id FROM plant_category WHERE id = :parent_id")
            parent_result = db.execute(parent_query, {"parent_id": parent_id}).fetchone()
            
            if not parent_result:
                return {"code": 200, "data": [], "message": "获取成功"}
            
            parent_plant_id = parent_result[0]
            # 计算父级的层级深度（点的数量）
            parent_level = parent_plant_id.count('.')
            # 查询直接子分类（层级深度+1）
            # 修复查询条件，使用更准确的正则表达式匹配
            query = text("""
                SELECT c.id, c.plant_name as name, c.plant_value as value,
                       (SELECT COUNT(*) FROM plant_category WHERE plant_id LIKE CONCAT(c.plant_id, '.%')) > 0 as hasChildren
                FROM plant_category c
                WHERE c.plant_id LIKE CONCAT(:parent_plant_id, '.%') 
                  AND LENGTH(c.plant_id) - LENGTH(REPLACE(c.plant_id, '.', '')) = :child_level
                ORDER BY c.plant_id
            """)
            # 执行查询并获取结果
            result = db.execute(query, {
                "parent_plant_id": parent_plant_id,
                "child_level": parent_level + 1
            }).fetchall()
        
        # 将结果转换为字典列表
        categories = []
        for row in result:
            categories.append({
                "id": row.id,
                "name": row.name,
                "value": row.value,
                "hasChildren": bool(row.hasChildren)
            })
        
        return {"code": 200, "data": categories, "message": "获取成功"}
    except Exception as e:
        # 记录错误详情
        print("===== 获取植物分类出错 =====")
        print(f"获取植物分类出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"code": 500, "message": f"获取失败: {str(e)}"}