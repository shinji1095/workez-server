# api/Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# PostgreSQL(psycopg系)のビルドに必要になりやすい
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# 依存を先に入れてレイヤキャッシュを効かせる
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# アプリ本体
COPY . /app

EXPOSE 8000

# config.wsgi はあなたのDjangoプロジェクト名に合わせてください
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
