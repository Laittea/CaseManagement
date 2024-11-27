FROM python:3.11-slim

WORKDIR /app

# 安装必要的系统包和 Python 开发工具
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 pip 和 setuptools
RUN pip install --no-cache-dir --upgrade pip setuptools

# 复制并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]