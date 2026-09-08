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
└── new example - 副本/     # uni-app 前端（v2.0 重构）
    ├── pages/
    │   ├── index/index.vue           # 启动页（品牌 + 登录/注册入口，已登录自动进入）
    │   ├── login/                    # login / register / findpassword（共用 auth.scss）
    │   ├── main/main.vue             # 主容器：自定义底部 Tab（首页 / 图鉴 / 识别 / 记录 / 我的）
    │   │   └── components/           # home-tab / atlas-tab / history-tab / mine-tab
    │   ├── identify/identify.vue     # 拍照 / 相册 → 上传识别 → 结果卡片（Top 5 + 置信度环）
    │   ├── plant/plantdetail.vue     # 植物详情（分类阶元 + 形态 / 环境 / 分布 / 习性 / 用途）
    │   └── about/about.vue           # 关于
    ├── components/                   # easycom 自动注册，无需 import
    │   ├── yl-navbar/                # 自定义导航栏（状态栏 / 胶囊避让、沉浸式）
    │   ├── yl-tabbar/                # 底部导航（中间凸起识别按钮）
    │   ├── yl-category-picker/       # 门→纲→目→科→属 逐级分类弹层
    │   ├── yl-plant-card/            # 植物卡片（无图时生成渐变封面）
    │   └── yl-empty/                 # 空状态
    ├── utils/
    │   ├── apiConfig.js              # 后端地址（可在「我的 → 服务器地址」中动态修改）
    │   ├── request.js                # uni.request / uploadFile 封装，统一解析 FastAPI 错误
    │   ├── api.js                    # 全部后端接口
    │   ├── auth.js                   # 登录态（token / userInfo）
    │   └── history.js                # 识别记录（本地存储）
    ├── static/                       # logo
    ├── uni_modules/uni-icons/        # 图标字体
    ├── App.vue                       # 全局样式 + globalData（不再承担页面切换）
    ├── uni.scss                      # 设计变量（$yl-* 品牌色 / 圆角 / 阴影）
    ├── main.js
    ├── pages.json                    # 标准路由 + easycom 规则
    └── manifest.json                 # App 配置（含 Android 权限）
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

## 四、前端页面（uni-app · v2.0 重构）

启动方式：用 HBuilderX 打开 `new example - 副本/` 文件夹即可（首次运行会提示安装 sass 编译插件，确认安装）。

> v2.0 前端完全重写：改为 uni-app 标准路由（`pages.json` + `uni.navigateTo` / `uni.reLaunch`），
> 组件通过 easycom 自动注册，UI 采用「雨林绿」设计体系（`uni.scss` 中的 `$yl-*` 变量）。
> **后端接口与数据结构未做任何修改。**

### 页面流程图

```
[index 启动页]  ── 已登录自动进入 ──→ [main 主容器]
   ├── 登录 ──→ [login] ──→ [main]
   │              ├── 忘记密码 ──→ [findpassword]（验证码 → 弹窗显示密码，可复制）
   │              └── 注册 ──→ [register]（邮箱验证码 + 密码强度）──→ [login]
   └── 先随便逛逛 ──→ [main]（游客模式，识别 / 图鉴均可用）

[main 主容器]（自定义底部 Tab）
   ├── 首页   ：问候 + 搜索 + 识别主卡片 + 快捷入口 + 分类速览（门）+ 最近识别 + 小知识
   ├── 图鉴   ：全部植物网格 / 分类弹层（门→纲→目→科→属）/ 结果内搜索 / 下拉刷新 / 无限滚动
   │             └──→ [plantdetail 植物详情]
   ├── 识别(中间凸起按钮) ──→ [identify]：拍照 / 相册（≤ 9 张）→ 逐张上传 → Top 5 结果 + 置信度环
   ├── 记录   ：本机识别记录（按日期分组、展开候选、删除 / 清空）
   └── 我的   ：用户信息 + 统计 / 服务器地址 / 清除缓存 / 关于 / 退出登录
```

### 关键文件

| 文件 | 作用 |
|---|---|
| [pages.json](new%20example%20-%20%E5%89%AF%E6%9C%AC/pages.json) | 标准路由表 + easycom 规则（`yl-*` → `components/yl-*/yl-*.vue`） |
| [uni.scss](new%20example%20-%20%E5%89%AF%E6%9C%AC/uni.scss) | 设计变量：品牌色、文字色、圆角、阴影、渐变（自动注入所有 scss 样式块） |
| [App.vue](new%20example%20-%20%E5%89%AF%E6%9C%AC/App.vue) | 全局样式（按钮 / 卡片 / 标签 / 动画 / 骨架屏）与 `globalData` |
| [utils/apiConfig.js](new%20example%20-%20%E5%89%AF%E6%9C%AC/utils/apiConfig.js) | API 基础地址（默认 `http://localhost:8000`，支持本地覆盖） |
| [utils/request.js](new%20example%20-%20%E5%89%AF%E6%9C%AC/utils/request.js) | 请求封装：自动拼接 baseUrl、携带 token、解析 FastAPI `detail` 错误 |
| [utils/api.js](new%20example%20-%20%E5%89%AF%E6%9C%AC/utils/api.js) | 登录 / 注册 / 验证码 / 找回密码 / 分类 / 植物列表 / 上传识别 |
| [pages/main/main.vue](new%20example%20-%20%E5%89%AF%E6%9C%AC/pages/main/main.vue) | Tab 容器，四个 Tab 以组件常驻，切换无闪烁 |
| [components/yl-category-picker](new%20example%20-%20%E5%89%AF%E6%9C%AC/components/yl-category-picker/yl-category-picker.vue) | 分类弹层：按树深度（0-4）映射到 `phylum/class/order/family/genus_latin_name` |
| [pages/identify/identify.vue](new%20example%20-%20%E5%89%AF%E6%9C%AC/pages/identify/identify.vue) | 识别流程；结果自动写入本地记录（`utils/history.js`） |
| [pages/plant/plantdetail.vue](new%20example%20-%20%E5%89%AF%E6%9C%AC/pages/plant/plantdetail.vue) | 详情页，数据通过 `getApp().globalData.currentPlant` 传递（后端无按 id 查询接口） |

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

1. 安装 HBuilderX（uni-app 官方 IDE，需 Vue3 / Vite 版本）
2. 打开 `new example - 副本/` 目录
3. 运行 → 运行到浏览器 / 手机或模拟器（H5、Android、iOS、微信小程序均可）
4. 真机调试时修改 [apiConfig.js](new%20example%20-%20%E5%89%AF%E6%9C%AC/utils/apiConfig.js) 的 `baseUrl` 为电脑局域网 IP，
   或直接在 App 内「我的 → 服务器地址」中填写（保存在本地，优先级高于代码默认值）

> 也可以用 uni-app 的 Vite CLI 运行：把 `new example - 副本/` 的内容放入
> `uni-preset-vue#vite` 模板的 `src/` 目录，`npm install && npm run dev:h5`。

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
- ~~前端把 5+ 个独立页面改成 `uni-app` 标准路由~~（v2.0 已完成）
- 后端增加「按中文名 / 拉丁名搜索」与「按 id 查询植物详情」接口（前端目前在已加载结果内做本地搜索）
- 后端提供静态图片访问（`image_path` 目前多为空，前端会自动生成渐变封面兜底）
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
