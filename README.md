# 雨林通（YULIN TONG）项目说明

> 基于深度学习的植物识别系统
> FastAPI 后端 + uni-app 移动端

---

## 一、项目概览

「雨林通」是一款植物识别 App，用户可以：

- 📷 上传植物图片，通过 YOLO 模型自动识别物种
- 📚 浏览「植物图鉴」（按 门→纲→目→科→属 多级分类检索）
- 👤 注册 / 登录（邮箱 + 验证码 / 数字 user_id 登录）
- 🔐 找回密码（邮箱验证码）
- 🛡️ 管理员操作日志（admin_info 表）

### 技术栈

| 层 | 技术 |
|---|---|
| 移动端 | uni-app (Vue 3) + uni-ui |
| 后端框架 | FastAPI + Uvicorn |
| ORM | SQLAlchemy 2.x |
| 数据库 | MySQL 5.7（数据库名 `tables`） |
| 鉴权 | JWT（python-jose + passlib） |
| AI 模型 | Ultralytics YOLO（`best.pt`） |
| 邮件 | smtplib（QQ 邮箱 SMTP） |

### 目录结构

```
YULIN_TONG~/
├── fastapi-backend/        # Python 后端
│   ├── app/
│   │   ├── api/            # 路由层
│   │   ├── config/         # 配置（密钥、DB、邮件）
│   │   ├── core/           # 基础设施（DB session）
│   │   ├── models/         # SQLAlchemy 模型
│   │   ├── schemas/        # Pydantic 模型
│   │   └── services/       # 业务逻辑
│   ├── best.pt             # YOLO 训练好的模型
│   ├── main.py             # FastAPI 入口
│   ├── tables.sql          # 数据库建表 + 初始化数据（≈ 50 MB）
│   └── query               # 占位文件（空）
│
└── new example - 副本/     # uni-app 前端
    ├── pages/              # 页面
    │   ├── index/          # 启动页
    │   ├── login/          # 登录 / 注册 / 找回密码
    │   ├── Home/           # 主菜单
    │   ├── identify/       # 图片识别
    │   ├── plant/          # 植物图鉴
    │   └── about/          # 关于
    ├── components/         # 公共组件
    ├── static/             # 图片 / 图标
    ├── utils/              # API 工具
    ├── App.vue             # 单页应用入口
    ├── main.js
    ├── pages.json
    └── manifest.json       # App 配置（含 Android 权限）
```

---

## 二、数据库设计（MySQL `tables` 库）

| 表名 | 用途 | 关键字段 |
|---|---|---|
| `user_info` | 用户账号 | `id`, `user_id`(数字, 唯一), `password`, `email`, `create_time` |
| `captchas` | 邮箱验证码 | `id`, `email`, `captcha`, `created_at`, `expires_at` |
| `plant_info` | 植物详情（核心数据） | `id`, `species_latin_name`, `species_chinese_name`, `kingdom_*`, `phylum_*`, `class_*`, `order_*`, `family_*`, `genus_*`, `common_names`, `growth_environment`, `distribution`, `morphological_features`, `growth_habits`, `usage_value`, `image_path` |
| `plant_category` | 植物多级分类 | `id`, `plant_id`（如 `1.1.1.1.1`）, `plant_name`, `plant_value`（拉丁名） |
| `recognition_log` | 识别历史 | `id`, `user_id`, `recognition_time`, `plant_info_id` |
| `admin_info` | 管理员操作日志 | `id`, `operation`, `operation_time`, `target_table`, `target_id`, `result`, `admin_id`（带触发器约束） |

### 当前数据样本

- `plant_info`：约 20+ 条已录入的苔藓/角苔数据
- `plant_category`：多级分类目录（门→属，5 层结构）
- `user_info`：2 个测试用户
  - `user_id=1234567` / `password=1234567` / 邮箱 `sunhaoran_2022@qq.com`
  - `user_id=12345677` / `password=12345677` / 邮箱 `3033714509@qq.com`
- `captchas`：历史验证码记录

> ⚠️ 建表 SQL 文件 `tables.sql` 约 50 MB，全是 `INSERT` 数据。如需重新建库，可分批导入或使用 `mysqldump` 时排除 `INSERT` 部分。

---

## 三、后端 API（FastAPI）

服务地址：`http://localhost:8000`
Swagger 文档：`http://localhost:8000/docs`

### 1. 认证模块 `/api/auth/*` — [auth_router.py](fastapi-backend/app/api/auth_router.py)

| 方法 | 路径 | 说明 | 入参 | 出参 |
|---|---|---|---|---|
| POST | `/api/auth/login` | 登录 | `{"username": "数字 user_id", "password": "..."}` | `{code, message, data:{userId, username, token}}` |
| POST | `/api/auth/register` | 注册 | `{"username": "数字ID", "email", "password", "captcha"}` | `{message, user, status}` |
| POST | `/api/auth/get-captcha` | 发送注册验证码 | `{"email": "..."}` 或 `?email=` | `{message, status}` |
| POST | `/api/auth/forgot-password/captcha` | 发送找回密码验证码 | `{"email": "..."}` | 同上 |
| POST | `/api/auth/reset-password` | 验证码重置 | `{"email", "captcha"}` | `{success, password}`（⚠️ 真实返回原密码，极不安全） |
| GET | `/api/auth/me` | 当前用户信息 | Bearer Token | `{userId, username}` |

> ⚠️ **安全注意**：
> - `verify_password` 用的是**明文比较**（见 [auth_service.py:12](fastapi-backend/app/services/auth_service.py#L12)）
> - `user_service.create_user` 也是**明文存储**密码
> - `reset-password` 直接返回原密码（生产环境绝对禁止）

### 2. 植物模块 `/api/*` — [plant_router.py](fastapi-backend/app/api/plant_router.py)

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/plants/list` | 植物列表（支持按 phylum/class/order/family/genus 拉丁名过滤，分页 page/pageSize） |
| GET | `/api/plants/categories?parent_id=N` | 树形分类（0=顶级） |
| POST | `/api/upload/image` | 上传单张图片并识别（**当前已移除 token 校验**） |
| POST | `/api/upload/images` | 批量上传 + 识别（需要 Bearer Token） |

### 3. 识别逻辑 — [plant_service.py](fastapi-backend/app/services/plant_service.py)

```python
model = YOLO("best.pt")  # 应用启动时加载一次
results = model.predict(source=file_path, save=False, conf=0)
# 取置信度 Top 5（分类模式）
# 或每个检测框（目标检测模式）
```

返回结构：
```json
{
  "class": "角苔属",
  "confidence": 0.87
}
```

---

## 四、前端页面（uni-app）

启动方式：用 HBuilderX 打开 `new example - 副本/` 文件夹即可。

### 页面流程图

```
[index 启动页]
   ├── 登录 ──→ [login] ──→ [homepage 主菜单]
   │              ├── 忘记密码 ──→ [findPassword]
   │              └── 注册 ──→ [register] ──→ [registersuccess] ──→ [login]
   │                                  ↑ 需邮箱验证码
   └── 注册 ──→ [register] ─→ ...（同上）
                    ↓ 登录成功后
              [homepage 主菜单]
                 ├── 植物图鉴 ──→ [planthome 树形选择] ──→ [plantimage 详情]
                 ├── 植物识别 ──→ [identify 图片上传/拍照]
                 └── 关于 ──→ [about]
```

### 关键文件

| 文件 | 作用 |
|---|---|
| [App.vue](new%20example%20-%20%E5%89%AF%E6%9C%AC/App.vue) | 单页应用壳，通过 `currentPage` 状态切换页面（无路由） |
| [utils/apiConfig.js](new%20example%20-%20%E5%89%AF%E6%9C%AC/utils/apiConfig.js) | API 基础地址配置（默认 `http://localhost:8000`） |
| [utils/api.js](new%20example%20-%20%E5%89%AF%E6%9C%AC/utils/api.js) | API 调用封装（目前只封装了分类） |
| [pages/login/login.vue](new%20example%20-%20%E5%89%AF%E6%9C%AC/pages/login/login.vue) | 登录页（直接 fetch `/api/auth/login`） |
| [pages/identify/identify.vue](new%20example%20-%20%E5%89%AF%E6%9C%AC/pages/identify/identify.vue) | 图片选择 + 上传 + 识别 |
| [pages/plant/planthome.vue](new%20example%20-%20%E5%89%AF%E6%9C%AC/pages/plant/planthome.vue) | 树形分类检索（自研 `peng-tree` 组件） |

### 已声明的 Android 权限

`CAMERA`、`FLASHLIGHT`、`ACCESS_NETWORK_STATE`、`VIBRATE`、`WAKE_LOCK`、`WRITE_SETTINGS` 等（见 `manifest.json`）

---

## 五、运行步骤

### 后端

```bash
# 1. 启动 MySQL（root/root，库名 tables）

# 2. 导入数据（首次）
mysql -uroot -proot tables < fastapi-backend/tables.sql

# 3. 安装依赖
cd fastapi-backend
pip install fastapi uvicorn sqlalchemy pymysql python-dotenv \
            "python-jose[cryptography]" "passlib[bcrypt]" \
            pydantic python-multipart email-validator ultralytics

# 4. 启动
python main.py
# 访问 http://localhost:8000/docs
```

### 前端

1. 安装 HBuilderX（uni-app 官方 IDE）
2. 打开 `new example - 副本/` 目录
3. 运行 → 运行到手机或模拟器（Android/iOS/微信小程序均可）
4. 真机调试时修改 [apiConfig.js](new%20example%20-%20%E5%89%AF%E6%9C%AC/utils/apiConfig.js) 的 `baseUrl` 为电脑局域网 IP

---

## 六、当前已知问题与改进点

### 🐛 Bug / 隐患

1. **明文密码**：[auth_service.py:12](fastapi-backend/app/services/auth_service.py#L12) 与 [user_service.py:33](fastapi-backend/app/services/user_service.py#L33) 都没有哈希
2. **登录逻辑**：`/api/auth/login` 只接受数字 user_id，不支持邮箱登录（前端用户体验差）
3. **`/api/upload/image` 移除了鉴权**（[plant_router.py:142-152](fastapi-backend/app/api/plant_router.py#L142-L152)），存在滥用风险
4. **`/api/auth/reset-password` 返回原密码**（[auth_router.py:230-237](fastapi-backend/app/api/auth_router.py#L230-L237)），严重安全漏洞
5. **YOLO 模型相对路径**：直接写 `"best.pt"`，部署时必须保证 CWD 是项目根
6. **SMTP 调试信息泄露**：[captcha_service.py:81-95](fastapi-backend/app/services/captcha_service.py#L81-L95) 启用了 `set_debuglevel(1)`，会在控制台打印所有 SMTP 交互

### ⚠️ 警告

- `bcrypt 4.x` 与 `passlib 1.7.4` 不兼容（提示 `module 'bcrypt' has no attribute '__about__'`）— 降级 `bcrypt<4` 或改用 `argon2`
- `pydantic` v2：`orm_mode` 已改名为 `from_attributes`
- `FastAPI on_event` 已 deprecated，建议改用 `lifespan`

### 💡 功能扩展建议

- 加一个「邮箱登录」接口
- 识别结果落库到 `recognition_log`（当前接口没写）
- 前端把 5+ 个独立页面改成 `uni-app` 标准路由（现在用 `currentPage` 字符串判断，文件多了难维护）
- 把 `tables.sql` 拆成 `schema.sql` + `data.sql`，方便重建
- 给 `best.pt` 加 Git LFS 或说明下载方式

---

## 七、常用命令速查

```bash
# 启动后端
cd fastapi-backend && python main.py

# 查看数据库
mysql -uroot -proot -e "USE tables; SHOW TABLES; SELECT COUNT(*) FROM plant_info;"

# 调用登录
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"1234567","password":"1234567"}'

# 上传图片识别
curl -X POST http://localhost:8000/api/upload/image \
  -F "file=@some_plant.jpg"
```
