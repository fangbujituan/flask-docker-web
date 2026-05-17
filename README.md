# Flask MySQL Docker 项目

一个简单的 Flask 应用，支持 MySQL 数据库和 Docker 部署。

## 项目结构

```
.
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   └── routes/
│       ├── __init__.py
│       ├── main.py
│       └── api.py
├── config.py
├── run.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## 快速开始

### 本地开发

1. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
.\venv\Scripts\activate  # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 复制 `.env.example` 为 `.env` 并配置数据库：
```bash
cp .env.example .env
```

4. 运行应用：
```bash
python run.py
```

### Docker 部署

1. 使用 Docker Compose 构建并运行：
```bash
docker-compose up --build
```

2. 访问应用：`http://localhost:5000`

## API 接口

- `GET /` - 首页
- `GET /health` - 健康检查
- `GET /api/users` - 获取所有用户
- `POST /api/users` - 创建新用户
- `GET /api/users/<id>` - 获取指定用户

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| MYSQL_HOST | MySQL 主机 | localhost |
| MYSQL_PORT | MySQL 端口 | 3306 |
| MYSQL_USER | MySQL 用户 | root |
| MYSQL_PASSWORD | MySQL 密码 | - |
| MYSQL_DATABASE | 数据库名 | flask_app |
| SECRET_KEY | Flask 密钥 | dev-secret-key |
