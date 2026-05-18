# Flask MySQL Docker 项目

一个完整的 Flask 全栈应用，支持 MySQL 数据库和 Docker 部署。

## 项目结构

```
.
├── app/                      # 后端应用
│   ├── __init__.py           # 应用工厂
│   ├── models/               # 数据模型
│   │   ├── __init__.py
│   │   └── user.py
│   └── routes/               # 路由蓝图
│       ├── __init__.py
│       ├── main.py           # 主路由
│       └── api.py            # API 接口
├── client/                   # 前端应用（Vue 3）
│   ├── src/
│   │   ├── main.js           # 入口文件
│   │   ├── App.vue           # 根组件
│   │   ├── router/           # 路由配置
│   │   └── views/            # 页面组件
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── config.py                 # 配置文件
├── run.py                    # 启动文件
├── requirements.txt          # Python 依赖
├── Dockerfile                # Docker 镜像构建
├── docker-compose.yml        # Docker 编排
├── .env.example              # 环境变量示例
├── .gitignore
└── README.md
```

## 技术栈

**后端：**
- Flask 3.0
- Flask-SQLAlchemy
- PyMySQL
- Gunicorn

**前端：**
- Vue 3
- Vue Router
- Vite

**数据库：**
- MySQL 8.0

**部署：**
- Docker
- Docker Compose

## 快速开始

### 本地开发

**1. 后端**

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入数据库配置

# 运行
python run.py
```

**2. 前端**

```bash
cd client

# 安装依赖
npm install

# 运行开发服务器
npm run dev
```

**3. 访问**

- 前端：http://localhost:3000
- 后端 API：http://localhost:22048

### Docker 部署

**1. 创建环境变量文件**

```bash
cat > .env << 'EOF'
MYSQL_HOST=host.docker.internal
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=你的密码
MYSQL_DATABASE=design
SECRET_KEY=your_secret_key
PORT=22048
EOF
```

**2. 构建并启动**

```bash
docker compose up -d --build
```

**3. 查看日志**

```bash
docker compose logs -f
```

**4. 停止服务**

```bash
docker compose down
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | / | 首页 |
| GET | /health | 健康检查 |
| GET | /api/users | 获取所有用户 |
| POST | /api/users | 创建用户 |
| GET | /api/users/:id | 获取指定用户 |

**创建用户示例：**

```bash
curl -X POST http://localhost:22048/api/users \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "email": "test@example.com"}'
```

## 前端页面

| 路径 | 说明 |
|------|------|
| / | 首页 |
| /users | 用户列表 |

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| MYSQL_HOST | MySQL 主机 | localhost |
| MYSQL_PORT | MySQL 端口 | 3306 |
| MYSQL_USER | MySQL 用户 | root |
| MYSQL_PASSWORD | MySQL 密码 | - |
| MYSQL_DATABASE | 数据库名 | flask_app |
| SECRET_KEY | Flask 密钥 | dev-secret-key |
| PORT | 应用端口 | 22048 |

## 常用命令

**后端：**

```bash
# 运行开发服务器
python run.py

# 使用 gunicorn 运行
gunicorn --bind 0.0.0.0:22048 run:app
```

**前端：**

```bash
cd client

# 开发
npm run dev

# 构建
npm run build

# 预览构建结果
npm run preview
```

**Docker：**

```bash
# 构建并启动
docker compose up -d --build

# 查看日志
docker compose logs -f

# 重启
docker compose restart

# 停止并删除
docker compose down
```
