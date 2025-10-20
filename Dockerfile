# 使用一个轻量级的 Python 官方镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# --- Dockerfile 修改开始 ---

# 1. 复制依赖文件
COPY requirements.txt .

# 2. 安装依赖
# --no-cache-dir 选项可以减小镜像大小
RUN pip install --no-cache-dir -r requirements.txt

# 3. 只复制您的主应用文件
COPY app.py .

# 4. 只复制 templates 文件夹及其内容
# COPY <源路径> <目标路径>
COPY templates/ ./templates/

# --- Dockerfile 修改结束 ---

# 暴露应用运行的端口
EXPOSE 5000

# 使用 gunicorn 启动应用
# --bind 0.0.0.0:5000 表示监听所有网络接口的 5000 端口
# app:app 表示运行 app.py 文件中的 app 实例
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]