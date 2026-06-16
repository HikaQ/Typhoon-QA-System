# 台风知识问答系统

基于知识图谱与 LLM 的台风知识问答系统，支持台风数据的智能检索与问答。

## 项目结构

```
Typhoon_System/
├── typhoon_request/    # 台风数据导入模块
│   ├── data_process.py     # 数据预处理（IBTrACS → CSV）
│   ├── typhoon_import.py   # Neo4j 知识图谱导入
│   ├── china_typhoon_list_2000_2026.csv   # 台风列表
│   └── china_typhoon_path_2000_2026.csv   # 路径点数据
├── web-flask/          # 后端服务 (Flask)
│   ├── app.py          # Flask 主入口
│   ├── init_db.py      # 数据库初始化脚本
│   ├── config.json     # LLM API 配置
│   ├── .env            # MySQL 数据库配置
│   └── requirements.txt
├── web-vue/            # 前端应用 (Vue 3 + Vite)
│   ├── src/
│   │   ├── api/        # API 接口层
│   │   ├── assets/     # 静态资源
│   │   ├── layouts/    # 布局组件
│   │   ├── router/     # 路由配置
│   │   ├── utils/      # 工具函数
│   │   └── views/      # 页面视图
│   ├── public/
│   └── package.json
├── start.bat           # 一键启动脚本 (Windows)
└── README.md
```

## 环境要求

| 依赖      | 说明                              |
| --------- | --------------------------------- |
| Python    | 3.9+ (推荐使用 Conda 管理环境)    |
| Node.js   | 18+ (用于前端开发和构建)           |
| Neo4j     | 图数据库，存储台风知识图谱         |
| MySQL     | 关系型数据库，存储业务数据         |

## 快速开始

### 1. 克隆项目

```bash
cd Typhoon_System
```

### 2. 数据库初始化

#### Neo4j（图数据库）

##### 安装与创建数据库

1. 前往 [Neo4j 官网](https://neo4j.com/download/) 下载并安装 `neo4j-desktop-2.1.4-x64.exe`
2. 在 Neo4j Desktop 中创建数据库，参数如下：

| 参数      | 值           |
| --------- | ------------ |
| Version   | 2026.04.0    |
| 数据库名  | typhoon      |
| 密码      | 12345678     |

##### 导入台风知识图谱数据

> 数据来源：[IBTrACS (NOAA)](https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/) — 国际气候管理最佳路径档案

**Step 1：下载原始数据**

从 NOAA 下载西北太平洋区域台风数据：

```
文件名：ibtracs.WP.list.v04r01.csv
下载地址：https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.WP.list.v04r01.csv
```

下载后放入 `typhoon_request/` 目录。

**Step 2：数据预处理**

筛选中国区域（经纬度 + 年份）的台风数据：

```bash
cd typhoon_request
python data_process.py
```

将生成三个文件：
- `china_typhoon_list_2000_2026.csv` — 台风列表
- `china_typhoon_path_2000_2026.csv` — 路径点数据
- `sample_typhoon.csv` — 演示用样本

**Step 3：导入 Neo4j**

```bash
python typhoon_import.py
```

##### 知识图谱结构

运行导入后，Neo4j 中将建立以下图谱：

| 节点类型    | 说明           | 属性                          |
| ----------- | -------------- | ----------------------------- |
| Typhoon     | 台风           | sid, name, season             |
| PathPoint   | 路径点         | lat, lon, wind, pressure, time |
| Year        | 年份           | value                         |
| Level       | 台风强度等级   | value（热带低压/热带风暴/台风/强台风/超强台风） |
| Date        | 日期           | value                         |
| Province    | 登录省份       | name（广东/福建/浙江/海南）    |

| 关系          | 方向                    |
| ------------- | ----------------------- |
| HAS_PATH      | Typhoon → PathPoint     |
| OCCURRED_IN   | Typhoon → Year          |
| HAS_LEVEL     | Typhoon → Level         |
| HAS_DATE      | Typhoon → Date          |
| LANDED_IN     | Typhoon → Province      |

#### MySQL（关系型数据库）

1. 确保 MySQL 服务已启动
2. 运行初始化脚本：

```bash
cd web-flask
python init_db.py
```

### 3. 启动后端

```bash
# 安装 Python 依赖
pip install -r web-flask/requirements.txt

# 启动 Flask 服务（端口 5000）
cd web-flask
conda run -n typhoon_system python app.py
```

后端 API 地址：[http://127.0.0.1:5000](http://127.0.0.1:5000)

### 4. 启动前端

```bash
# 安装 npm 依赖（仅第一次）
cd web-vue
npm install

# 启动开发服务器（端口 5173）
npm run dev
```

前端页面地址：[http://localhost:5173](http://localhost:5173)

### 5. 一键启动 (Windows)

双击根目录下的 `start.bat`，脚本将自动启动 MySQL、后端、前端三个服务。

## 配置修改

拿到项目后，需要修改以下配置文件，替换为你自己的连接信息和 API 密钥。

### 1. LLM API 配置 — `web-flask/config.json`

```json
{
  "siliconflow": {
    "api_key": "换成你的 API Key",
    "base_url": "https://api.siliconflow.cn/v1/chat/completions",
    "model": "deepseek-ai/DeepSeek-V4-Flash",
    "timeout": 60
  }
}
```

| 字段       | 说明                                                   |
| ---------- | ------------------------------------------------------ |
| `api_key`  | SiliconFlow API 密钥，[注册获取](https://siliconflow.cn) |
| `base_url` | API 请求地址，无需改动                                  |
| `model`    | 使用的模型，可按需切换                                  |
| `timeout`  | 请求超时时间（秒）                                       |

### 2. MySQL 数据库配置 — `web-flask/.env`

```env
MYSQL_HOST=localhost          # 数据库地址
MYSQL_PORT=3306               # 数据库端口
MYSQL_USER=root               # 你的 MySQL 用户名
MYSQL_PASSWORD=admin          # 你的 MySQL 密码
MYSQL_DATABASE=typhoon_system # 数据库名称
```

### 3. Neo4j 图数据库配置 — `web-flask/algo/knowledge_graph/config.py`

```python
NEO4J_URI = "neo4j://127.0.0.1:7687"   # Neo4j 地址和端口
NEO4J_USER = "neo4j"                     # Neo4j 用户名
NEO4J_PASSWORD = "12345678"              # Neo4j 密码
```

### 4. 前端代理配置 — `web-vue/vite.config.js`

```js
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/log': {
        target: 'http://localhost:5000', // 后端地址，改端口改这里
        changeOrigin: true,
        rewrite: (path) => path,
      },
      '/user': 'http://localhost:5000',              // 同上
      '/conversation': 'http://localhost:5000',      // 同上
      '/knowledge_graph': 'http://localhost:5000'    // 同上
    }
  }
})
```

> **注意**：如果后端端口不是 `5000`，需要将上述 4 个 `target` 中的端口号都改掉。

### 5. 后端端口 — `web-flask/app.py`

默认端口 `5000`，如需修改：

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # 改 port 参数
```

---

⚠️ **安全提醒**：以上配置文件包含敏感信息（密码、API Key），请不要将填写真实值后的配置提交到公开仓库。建议将 `config.json`、`.env`、`config.py` 加入 `.gitignore`。

## 测试账号

| 角色   | 用户名     | 密码           |
| ------ | ---------- | -------------- |
| 管理员 | admin      | admin123456    |
| 普通用户 | testuser | test123456     |

## 常见问题

**PowerShell 报脚本执行策略错误**

以管理员身份打开 PowerShell，执行：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**前端 `npm run dev` 报错**

```bash
# 删除 node_modules 重新安装
rm -rf node_modules package-lock.json
npm install
```

**后端连接 Neo4j 失败**

确保 Neo4j Desktop 中对应的数据库已启动，且密码配置与 `web-flask/app.py` 中一致。

## 技术栈

- **后端**: Flask + SQLAlchemy + PyMySQL + Neo4j
- **前端**: Vue 3 + Vue Router + Axios + Vite
- **数据库**: MySQL + Neo4j（图数据库）
