# 台风灾害知识问答系统 - 完整使用说明

## 项目概述

本项目是一个基于 **知识图谱(Neo4j)** 和 **大语言模型(LLM)** 的 图检索增强(GraphRAG) 的 **台风灾害智能问答系统**。系统采用前后端分离架构，为用户提供精准的台风灾害领域知识查询和智能问答服务。

### 核心特色
- ✅ **知识图谱驱动**：基于Neo4j图数据库的复杂实体关系网络
- ✅ **GraphRAG技术**：图检索增强生成，提供更精准的问答能力
- ✅ **智能对话**：集成大语言模型(Qwen/DeepSeek)API
- ✅ **文档管理**：支持多种格式(Word/PDF)的文档上传和处理
- ✅ **可视化展示**：交互式知识图谱可视化界面

---

## 🛠️ 工具与技术栈详解

### 前端技术栈

| 工具 | 版本 | 用途 |
|------|------|------|
| **Vue** | 3.5.24 | 渐进式JavaScript框架，实现UI交互 |
| **Vue Router** | 4.6.4 | 单页应用路由管理，页面导航 |
| **Axios** | 1.13.2 | HTTP客户端库，调用后端API |
| **Vite** | 7.2.4 | 现代化前端构建工具，快速开发环境 |
| **Element Plus** | 最新版 | UI组件库，构建用户界面(预期) |
| **ECharts** | 最新版 | 数据可视化库，知识图谱展示(预期) |
| **Pinia** | 最新版 | Vue3状态管理库(预期) |

### 后端技术栈

| 工具 | 版本 | 用途 |
|------|------|------|
| **Flask** | 最新版 | Python轻量级Web框架 |
| **Flask-CORS** | 最新版 | 跨域资源共享(CORS)支持 |
| **SQLite** | 内置 | 轻量级关系型数据库(本地存储) |
| **PyJWT** | 最新版 | JWT令牌认证 |
| **Requests** | 最新版 | HTTP客户端库 |
| **python-docx** | 最新版 | Word(.docx)文档处理 |
| **PyPDF2** | 最新版 | PDF文档处理 |

### 算法与数据库

| 工具 | 版本 | 用途 |
|------|------|------|
| **Neo4j** | 4.4+ | 图数据库，存储知识图谱 |
| **Neo4j Python Driver** | 最新版 | Neo4j官方Python客户端 |
| **Qwen API / DeepSeek API** | 接口版 | 大语言模型，文本理解与生成 |
| **SiliconFlow SDK** | 最新版 | LLM API统一调用接口 |

---

## 🏗️ 系统架构

### 整体架构图

**层级架构**

| 层级 | 组件 | 功能 | 端口 |
|------|------|------|------|
| **前端层** | Vue3 + Vite | 登录注册、用户管理、文档管理、知识图谱管理、智能问答、会话管理 | 5173 |
| **后端API层** | Flask | /user、/chat、/kg、/document 路由 | 5010 |
| **GraphRAG处理层** | 算法引擎 | 实体抽取 → 图检索 → 上下文构建 → Prompt生成 → LLM调用 | 内部 |
| **数据处理层** | SQLite + 文档解析 | 用户、文档、对话、问答记录存储，Word/PDF处理 | 本地 |
| **图数据库层** | Neo4j | 知识图谱存储（节点、关系、灾害信息） | 7687 |
| **LLM服务层** | SiliconFlow API | Qwen/DeepSeek 大语言模型调用 | 云端 |

**请求流程**

```
客户端浏览器 (http://localhost:5173)
         ↓ Axios HTTP 请求
    Flask 后端 (http://localhost:5010)
         ↓
    ┌─────────────────────────
    │ GraphRAG 处理流程:       
    │ 1. 实体抽取             
    │ 2. 知识图谱检索         
    │ 3. 上下文构建           
    │ 4. Prompt 生成          
    │ 5. LLM 调用             
    └─────────────────────────
         ↓              ↓
    Neo4j 图数据库     LLM API
    (bolt://localhost:7687)  (SiliconFlow)
         ↓              ↓
       知识图谱         生成答案
         ↓              ↓
    ─────────────────────────
         ↓
    返回最终答案给用户
```

### GraphRAG 核心处理流程

**步骤流程图**

```
输入 → 处理 → 输出
─────────────────────────────────────────────────────

[用户问题] "2023年福建台风灾害"
    ↓
[1️⃣ 实体抽取]
   提取关键信息: year=2023, province=福建
   方法: 正则表达式匹配
    ↓
[2️⃣ 知识图谱检索]
   在 Neo4j 中执行 Cypher 查询
   查询语句:
   MATCH (t:Typhoon)-[:LANDED_IN]->(p:Province {name:'福建'})
          -[:OCCURRED_IN]->(y:Year {value:2023})
   RETURN t.name, t.intensity, t.impact
    ↓
[3️⃣ 上下文构建]
   组织检索结果成结构化文本
   格式: 
   - 台风名称: 杜苏芮
   - 强度: 12级
   - 登陆地点: 福建
   - 灾害影响: 洪水、滑坡、风灾
    ↓
[4️⃣ Prompt 生成]
   合并系统指令 + 用户问题 + 检索上下文
   prompt = "根据以下知识图谱信息，回答问题..."
    ↓
[5️⃣ LLM 调用]
   发送 POST 请求到 SiliconFlow API
   调用 Qwen 或 DeepSeek 模型
    ↓
[✅ 生成答案]
   "2023年福建地区受到台风杜苏芮影响，该台风强度达到12级..."
    ↓
[返回用户] JSON 格式响应
{
  "answer": "生成的答案文本",
  "context": "检索的上下文信息",
  "entities": {"year": 2023, "province": "福建"}
}
```

**各模块对应关系**

| GraphRAG组件 | 对应代码模块 | 核心逻辑 |
|-------------|-----------|--------|
| 实体抽取 | `triplet_extractor.py` | 正则表达式提取年份、地点 |
| 知识图谱检索 | `graph_retriever.py` | Neo4j Cypher 查询 |
| 上下文构建 | `context_builder.py` | 组织检索数据成文本 |
| Prompt构建 | `prompt_builder.py` | Prompt 模板 + 数据填充 |
| LLM调用 | `llm_client.py` | SiliconFlow API 调用 |
| 对话入口 | `conversation.py` | 路由 /chat/ask 端点 |

---

## 项目目录结构详解

```
typhoon-disaster-graphrag-web/
│
├── web-flask/                              # Flask后端项目
│   ├── app.py                              # Flask应用主入口
│   ├── config.json                         # 配置文件(LLM API密钥)
│   ├── init_db.py                          # 数据库初始化脚本
│   ├── test_chat.py                        # 测试脚本
│   ├── requirements.txt                    # Python依赖列表
│   │
│   ├── algo/                               # 算法模块
│   │   ├── llm/                            # 大语言模型服务
│   │   │   ├── llm_client.py               # LLM API客户端封装
│   │   │   ├── prompt_builder.py           # Prompt构建模块
│   │   │   └── config.py                   # LLM配置
│   │   │
│   │   └── knowledge_graph/                # 知识图谱处理
│   │       ├── neo4j_client.py             # Neo4j连接管理
│   │       ├── triplet_extractor.py        # 三元组提取(实体抽取)
│   │       ├── graph_retriever.py          # 知识图谱检索
│   │       ├── context_builder.py          # 上下文构建
│   │       └── config.py                   # Neo4j配置
│   │
│   ├── routes/                             # API路由
│   │   ├── user.py                         # 用户管理API (/user)
│   │   ├── conversation.py                 # 对话API (/chat)
│   │   ├── knowledge_graph.py              # 知识图谱API (/kg)
│   │   └── document.py                     # 文档管理API (预期)
│   │
│   └── utils/                              # 工具模块
│       ├── db.py                           # 数据库连接
│       ├── models.py                       # SQLAlchemy数据模型
│       └── security_utils.py               # 安全工具(密码哈希等)
│
├── web-vue/                                # Vue3前端项目
│   ├── index.html                          # HTML入口
│   ├── package.json                        # NPM依赖配置
│   ├── vite.config.js                      # Vite构建配置
│   ├── README.md                           # 前端说明
│   │
│   ├── public/                             # 静态资源文件夹
│   │
│   └── src/                                # 源代码
│       ├── main.js                         # Vue入口文件
│       ├── App.vue                         # 根组件
│       │
│       ├── api/                            # API服务层
│       │   ├── chat.js                     # 对话API调用
│       │   ├── request.js                  # HTTP请求封装
│       │   └── ...其他API模块
│       │
│       ├── views/                          # 页面组件
│       │   ├── Login.vue                   # 登录页面
│       │   ├── Register.vue                # 注册页面
│       │   ├── User.vue                    # 用户端主页
│       │   ├── AdminLogin.vue              # 管理端登录
│       │   ├── Setting.vue                 # 设置页面
│       │   ├── Log.vue                     # 日志页面
│       │   └── ...其他页面
│       │
│       ├── layouts/                        # 布局组件
│       │   ├── AdminLayout.vue             # 管理端布局
│       │   └── UserLayout.vue              # 用户端布局
│       │
│       ├── router/                         # 路由配置
│       │   └── index.js                    # 路由定义
│       │
│       ├── assets/                         # 静态资源
│       │   └── global.css                  # 全局样式
│       │
│       └── ...其他组件和工具
│
└── 文档资源/
    ├── 项目介绍文档.md
    ├── 数据库表结构说明.md
    └── ...其他文档
```

---

## 数据库结构

### SQLite数据表

#### 1. **user表** - 用户信息
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    email VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',           -- 'admin' 或 'user'
    avatar_url VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);
```

#### 2. **document表** - 文档信息
```sql
CREATE TABLE document (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    filename VARCHAR(200) NOT NULL,
    file_path VARCHAR(500),
    file_size INTEGER,
    file_type VARCHAR(20),                     -- 'pdf', 'docx', 'txt'
    content TEXT,                              -- 提取的文本内容
    upload_user_id INTEGER,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    kg_status VARCHAR(20) DEFAULT 'pending',   -- 'pending', 'processing', 'completed', 'failed'
    FOREIGN KEY (upload_user_id) REFERENCES user(id)
);
```

#### 3. **conversation表** - 对话会话
```sql
CREATE TABLE conversation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

#### 4. **qa_history表** - 问答记录
```sql
CREATE TABLE qa_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT,
    context TEXT,                              -- GraphRAG检索结果
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversation(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

#### 5. **typhoon_info表** - 台风档案
```sql
CREATE TABLE typhoon_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    typhoon_name VARCHAR(100) NOT NULL,
    typhoon_number VARCHAR(20),
    year INTEGER,
    intensity VARCHAR(50),                     -- '超强台风', '强台风', etc
    landing_location VARCHAR(200),
    max_wind_speed FLOAT,
    arrival_time TIMESTAMP,
    summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 6. **typhoon_case表** - 灾害案例
```sql
CREATE TABLE typhoon_case (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    typhoon_id INTEGER,
    case_title VARCHAR(200),
    location VARCHAR(200),
    disaster_type VARCHAR(100),                -- '洪水', '滑坡', '风灾', etc
    damage_description TEXT,
    casualties_count INTEGER,
    economic_loss FLOAT,
    relief_measures TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (typhoon_id) REFERENCES typhoon_info(id)
);
```

### Neo4j知识图谱结构

#### 节点类型 (Node Types)
```
Typhoon        - 台风
├─ 属性: name, number, intensity, year, description

Province       - 省份
├─ 属性: name, code

Year           - 年份
├─ 属性: value

Level          - 风力等级
├─ 属性: value (例: "12级", "13级")

Impact         - 灾害影响
├─ 属性: type, description, severity

Date           - 日期
├─ 属性: value

Relief         - 救援信息
├─ 属性: type, description
```

#### 关系类型 (Relationship Types)
```
Typhoon -[OCCURRED_IN]-> Year          # 台风发生的年份
Typhoon -[LANDED_IN]-> Province        # 台风登陆的省份
Typhoon -[HAS_LEVEL]-> Level           # 台风的风力等级
Typhoon -[HAS_DATE]-> Date             # 台风的日期
Typhoon -[HAS_IMPACT]-> Impact         # 台风的灾害影响
Typhoon -[HAS_RELIEF]-> Relief         # 台风的救援措施
Impact -[AFFECTED_AREA]-> Province     # 灾害影响的地区
```

---

## 安装与配置

### 前置要求
- Python 3.8+
- Node.js 16.0+
- Neo4j 4.4+
- API密钥(Qwen或DeepSeek)

### 第一步：安装Neo4j数据库

#### Windows安装步骤
1. 下载Neo4j Desktop: https://neo4j.com/download/
2. 安装并打开Neo4j Desktop
3. 创建新的本地数据库实例
4. 启动数据库服务
5. 初始登录 `neo4j / neo4j`
6. **重要**: 首次登录需要修改密码为 `neo4j123`
   - 系统配置文件中默认密码为: `neo4j123`
7. 访问 `http://localhost:7474` 查看图数据库

#### 验证Neo4j连接
```bash
# 在Neo4j浏览器中运行
RETURN "Neo4j is running" AS status
```

### 第二步：后端配置与启动

#### 2.1 配置LLM API

编辑 `web-flask/config.json` 文件:

```json
{
  "siliconflow": {
    "api_key": "sk-你的API密钥",
    "base_url": "https://api.siliconflow.cn/v1/chat/completions",
    "model": "Pro/deepseek-ai/DeepSeek-V3.2",
    "timeout": 20
  }
}
```

**获取API密钥步骤:**
1. 访问硅基流动平台: https://api.siliconflow.cn/
2. 注册账号并登录
3. 创建API密钥
4. 将密钥复制到 `config.json` 的 `api_key` 字段

#### 2.2 配置Neo4j连接

编辑 `web-flask/algo/knowledge_graph/config.py`:

```python
# Neo4j连接配置
NEO4J_URI = "neo4j://localhost:7687"       # Neo4j服务地址
NEO4J_USER = "用户名"                      # 用户名
NEO4J_PASSWORD = "密码"               # 密码(必须与数据库密码一致)
```

#### 2.3 安装Python依赖

```bash
cd web-flask

# 创建虚拟环境(可选但推荐)
python -m venv venv
# Windows激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

#### 2.4 初始化数据库

```bash
# 初始化SQLite数据库
python init_db.py

# 输出应显示:
# Created all tables
# 创建默认用户...
# Admin user created
```

#### 2.5 启动后端服务

```bash
# 启动Flask服务器
python app.py

# 输出应显示:
# WARNING in app.run(), this is a development server...
# Running on http://127.0.0.1:5010
```

**后端服务已启动**，默认运行在 `http://localhost:5010`

### 第三步：前端配置与启动

#### 3.1 安装Node依赖

```bash
cd web-vue

# 安装依赖
npm install

# 或使用yarn
yarn install
```

#### 3.2 启动前端开发服务器

```bash
# 启动开发服务器
npm run dev

# 输出应显示:
# VITE v7.2.4  ready in 234 ms
#
# ➜  Local:   http://localhost:5173/
# ➜  press h to show help
```

**前端已启动**，访问 `http://localhost:5173`

#### 3.3 生产环境构建

```bash
# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

---

## 💻 使用方法

### 账号登录

#### 默认账号
- **管理员账号**: `admin` / `123456`
- **普通用户账号**: `test` / `123456`

#### 用户注册
1. 点击"注册"链接
2. 输入用户名和密码
3. 完成注册后即可登录

### 用户功能

#### 1. 智能问答 (核心功能)

**使用流程:**
1. 登录系统，进入"问答"页面
2. 在对话框输入问题(例: "2024年福建台风灾害情况?")
3. 系统自动进行GraphRAG处理:
   - 提取实体(年份、地点、台风名)
   - 在知识图谱中检索相关数据
   - 构建上下文信息
   - 调用LLM生成回答
4. 查看系统返回的答案
5. 可继续提出后续问题进行多轮对话

**问题示例:**
```
- "2023年浙江受哪些台风影响?"
- "台风杜苏芮的强度和登陆地点?"
- "广东地区的台风灾害有哪些?"
- "历史上最强的台风是?"
```

#### 2. 会话管理

- **创建会话**: 每个问答对话自动保存为一个会话
- **会话列表**: 查看历史会话记录，点击可恢复会话
- **删除会话**: 可删除不需要的会话记录
- **多线程对话**: 在不同会话中进行平行对话

### 管理员功能

#### 1. 文档管理

**上传文档:**
1. 进入"文档管理"页面
2. 点击"上传文档"按钮
3. 选择Word(.docx)或PDF文件
4. 输入文档标题
5. 点击"上传"提交

**支持格式:**
- `.docx` - Word文档
- `.pdf` - PDF文档
- `.txt` - 纯文本文件

#### 2. 知识图谱管理

**数据同步到图数据库 (重要!)**

**流程:**
1. 进入"知识图谱管理"
2. 点击"同步数据到图数据库"按钮
3. 系统自动执行:
   - 遍历所有上传的文档
   - 使用LLM提取实体和关系(三元组)
   - 创建或更新Neo4j中的节点和关系
   - 显示进度和状态

**工作流程详解:**
```
选择文档 → 三元组提取 → 数据验证 → Neo4j写入 → 完成
   ↓          ↓           ↓         ↓
文本解析   LLM分析    去重处理   创建节点
         关系提取    关系校验   生成关系
```

#### 3. 知识图谱可视化

**查看图谱:**
1. 进入"知识图谱可视化"页面
2. 系统自动加载Neo4j中的所有节点和关系
3. 使用鼠标操作:
   - 拖拽平移画布
   - 滚轮缩放
   - 点击节点查看详情

**筛选与搜索:**
- **节点类型筛选**: 按实体类型显示/隐藏节点
- **关系类型筛选**: 按关系类型显示/隐藏关系
- **节点搜索**: 输入节点名称搜索并高亮显示

#### 4. 用户管理

- **查看用户列表**: 所有注册用户
- **用户信息编辑**: 修改用户信息
- **密码重置**: 重置用户登录密码
- **用户删除**: 删除用户及其相关数据
- **角色管理**: 分配用户角色(admin/user)

#### 5. 统计仪表板

- **用户统计**: 注册用户数、活跃用户
- **文档统计**: 上传文档数量、类型分布
- **会话统计**: 总会话数、活跃会话
- **问答统计**: 系统回答问题数、平均响应时间

---

## 🔌 API文档

### 基础配置

```
基础URL: http://localhost:5010
认证方式: JWT token (登录后获取)
请求格式: JSON
响应格式: JSON
```

### 用户相关API

#### 1. 用户注册
```http
POST /user/register
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123"
}

响应:
{
  "msg": "注册成功"
}
```

#### 2. 用户登录
```http
POST /user/login
Content-Type: application/json

{
  "username": "admin",
  "password": "123456"
}

响应:
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

#### 3. 获取用户信息
```http
GET /user/profile
Authorization: Bearer {token}

响应:
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "role": "admin",
  "avatar_url": "http://...",
  "created_at": "2024-01-15 10:30:00"
}
```

### 对话相关API

#### 1. 发送问题和获取答案
```http
POST /chat/ask
Content-Type: application/json
Authorization: Bearer {token}

{
  "question": "2023年台湾的台风灾害"
}

响应:
{
  "answer": "根据知识图谱检索的结果，2023年台湾受到以下台风影响...",
  "context": {
    "entities": {"year": 2023, "province": "台湾"},
    "graph_data": {"typhoons": [...], "impacts": [...]},
    "related_info": "..."
  }
}
```

#### 2. 创建会话
```http
POST /chat/conversation/create
Content-Type: application/json
Authorization: Bearer {token}

{
  "title": "台风灾害咨询"
}

响应:
{
  "conversation_id": 5,
  "title": "台风灾害咨询",
  "created_at": "2024-03-25 10:00:00"
}
```

#### 3. 获取会话列表
```http
GET /chat/conversation/list
Authorization: Bearer {token}

响应:
{
  "conversations": [
    {
      "id": 1,
      "title": "2023台风咨询",
      "created_at": "2024-01-15",
      "message_count": 5
    },
    {
      "id": 2,
      "title": "灾害预防问题",
      "created_at": "2024-01-20",
      "message_count": 3
    }
  ]
}
```

### 知识图谱相关API

#### 1. 查询知识图谱
```http
POST /kg/query
Content-Type: application/json
Authorization: Bearer {token}

{
  "question": "2024年福建台风"
}

响应:
{
  "entities": {
    "year": 2024,
    "province": "福建",
    "typhoon": null
  },
  "graph_data": {
    "year": 2024,
    "province": "福建",
    "typhoons": [
      {"name": "台风甲", "level": "12级"},
      {"name": "台风乙", "level": "10级"}
    ]
  },
  "context": "2024年福建地区受到台风甲和台风乙的影响..."
}
```

#### 2. 获取知识图谱统计
```http
GET /kg/statistics
Authorization: Bearer {token}

响应:
{
  "node_count": 256,
  "relationship_count": 512,
  "node_types": {
    "Typhoon": 45,
    "Province": 15,
    "Year": 20,
    "Impact": 156,
    "Relief": 20
  },
  "relationship_types": {
    "OCCURRED_IN": 50,
    "LANDED_IN": 48,
    "HAS_IMPACT": 200,
    "HAS_RELIEF": 30
  }
}
```

---

## 🔧 故障排除

### 常见问题

#### 问题1: Neo4j无法连接
**错误信息:** `ConnectionError: Failed to connect to Neo4j`

**解决方案:**
1. 确认Neo4j服务正在运行
2. 检查 `config.py` 中的连接地址: `bolt://localhost:7687`
3. 验证用户名和密码是否为 `neo4j 123456`
4. 重启Neo4j服务

#### 问题2: LLM API调用失败
**错误信息:** `API Error: 401 Unauthorized` 或 `Timeout`

**解决方案:**
1. 检查 `config.json` 中的API密钥是否正确
2. 确认百炼平台账号余额充足
3. 检查网络连接
4. 增加超时时间: 在 `config.json` 中改为 `"timeout": 30`

#### 问题3: 前后端跨域访问问题
**错误信息:** `CORS error` 或 `Cross-Origin Request Blocked`

**解决方案:**
- 后端已配置CORS，确保前端请求URL正确
- 前端URL: `http://localhost:5173`
- 后端URL: `http://localhost:5010`
- 检查浏览器控制台的具体错误信息

#### 问题4: 文档上传失败
**错误信息:** `File format not supported`

**解决方案:**
1. 确保文件格式为 `.docx` 或 `.pdf`
2. 文件大小不超过500MB
3. 检查文件是否损坏，尝试重新打开文件
4. 查看后端日志获取详细错误

#### 问题5: 知识图谱查询没有结果
**症状:** 问答系统始终回答"无法找到相关信息"

**解决方案:**
1. **检查是否完成数据同步**:
   - 进入"知识图谱管理"
   - 点击"同步数据到图数据库"
   - 等待处理完成

2. **检查文档内容**:
   - 上传的文档必须包含台风、地点等相关信息
   - 可查看文档提取的文本内容

3. **补充知识数据**:
   - 根据需要上传更多相关文档
   - 运行数据同步更新知识图谱

#### 问题6: 用户登录失败
**错误信息:** `Invalid username or password`

**解决方案:**
1. 核对账号密码是否正确
2. 使用默认账号测试: `test / 123456`
3. 注册新账号进行测试
4. 检查SQLite数据库是否已初始化

---

## ⚙️ 系统配置详解

### 后端配置文件

#### 1. LLM配置 (`web-flask/algo/llm/config.py`)
```python
# 大语言模型配置
LLM_TYPE = "siliconflow"                    # LLM提供商
LLM_MODEL = "Pro/deepseek-ai/DeepSeek-V3.2" # 模型名称
LLM_TIMEOUT = 30                            # API超时时间(秒)
LLM_MAX_TOKENS = 2000                       # 最大token数
```

#### 2. Neo4j配置 (`web-flask/algo/knowledge_graph/config.py`)
```python
NEO4J_URI = "bolt://localhost:7687"         # Neo4j地址
NEO4J_USER = "neo4j"                        # 用户名
NEO4J_PASSWORD = "neo4j123"                 # 密码
NEO4J_POOL_SIZE = 50                        # 连接池大小
```

#### 3. Flask应用配置 (`web-flask/app.py`)
```python
DEBUG = True                                 # 调试模式
HOST = "0.0.0.0"                            # 监听地址
PORT = 5010                                 # 监听端口
```

### 前端配置

#### Vite配置 (`web-vue/vite.config.js`)
```javascript
export default {
  server: {
    port: 5173,                             // 开发服务器端口
    proxy: {
      '/api': {
        target: 'http://localhost:5010',    // 后端API代理
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
}
```

---

## 📝 开发工作流

### 添加新的问答功能

#### 第一步: 扩展实体抽取
编辑 `web-flask/algo/knowledge_graph/triplet_extractor.py`:
```python
def extract_entities(question: str):
    result = {
        "year": None,
        "province": None,
        "typhoon": None,           # 新增字段
        "disaster_type": None      # 新增字段
    }
    # 添加抽取逻辑
    return result
```

#### 第二步: 扩展图查询
编辑 `web-flask/algo/knowledge_graph/graph_retriever.py`:
```python
def retrieve_knowledge(entities):
    # 添加新的Cypher查询逻辑
    if entities.get("disaster_type"):
        cypher = """
        MATCH (i:Impact {type: $disaster_type})
        RETURN i.description AS description
        """
        # 执行查询...
```

#### 第三步: 测试
```bash
cd web-flask
python test_chat.py
```

---

## 📚 参考资源

### 官方文档
- **Neo4j**: https://neo4j.com/docs/
- **Qwen AI**: https://dashscope.console.aliyun.com/
- **Vue3**: https://vuejs.org/
- **Flask**: https://flask.palletsprojects.com/

### 相关资源
- **GraphRAG论文**: https://arxiv.org/abs/2404.16130
- **Cypher查询语言**: https://neo4j.com/docs/cypher-manual/
- **知识图谱教程**: https://kgbase.github.io/

---

## 🎓 重要提示与注意事项

### 必读!

1. **数据同步必须手动执行**
   - 上传文档后，需要进入"知识图谱管理"，点击"同步数据到图数据库"
   - 不执行同步，知识图谱不会更新！

2. **Neo4j密码修改**
   - 首次启动Neo4j后必须修改密码为 `neo4j123`
   - 密码必须与系统配置一致

3. **API密钥安全**
   - `config.json` 文件包含敏感信息
   - 不要将其提交到公共代码库
   - 线上部署时使用环境变量

4. **多用户同时登录**
   - 为避免会话冲突，建议使用不同浏览器
   - 推荐: Chrome (管理员) + Firefox (普通用户)

5. **文档格式注意**
   - Word文件必须是 `.docx` 格式(不支持 `.doc`)
   - PDF文件确保可以提取文字(不支持纯图片PDF)
   - 文件编码应为UTF-8

6. **生产环境部署**
   - 修改Flask调试模式为False: `debug=False`
   - 更改默认端口避免冲突
   - 配置HTTPS证书
   - 设置强密码和复杂的API密钥

---

## 📞 技术支持

如遇问题，请按以下步骤排查:

1. **检查日志**
   - 后端日志: 在Flask启动的终端查看
   - 前端日志: 浏览器开发者工具(F12) → Console

2. **验证服务状态**
   ```bash
   # 后端健康检查
   curl http://localhost:5010/health
   
   # 前端访问
   http://localhost:5173
   ```

3. **数据库检查**
   - Neo4j浏览器: http://localhost:7474
   - SQLite: 使用SQLiteBrowser查看数据

---

**文档更新日期**: 2024年3月25日  
**项目版本**: v1.0.0  
**技术栈**: Vue3 + Flask + Neo4j + LLM

