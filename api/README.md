# Django API Server (Django + DRF)

## 1. セットアップ（ローカル）

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/local.txt
```

環境変数（例）:

```bash
cp .env.example .env.local
# 値を埋める
export ENV_FILE=.env.local
export DJANGO_SETTINGS_MODULE=config.settings.local
```

DB作成:

```bash
python manage.py migrate
```

起動:

```bash
python manage.py runserver 0.0.0.0:8000
```

## 2. 認証（暫定実装）

JWT を利用します。まず API キーでトークンを発行し、以降は Bearer JWT を使います。

### トークン発行
- エンドポイント: `POST /auth/token`
- ヘッダ: `X-API-KEY: <key>`（互換用に `Authorization: Bearer <key>` も許可）
- ボディ: `{"sub": "<subject>"}`（例: `admin-1` / `user-1` / `device-1`）
- ロール:
  - `ADMIN_API_KEY` → admin
  - `USER_API_KEY` → user（一般）
  - `DEVICE_API_KEY` → device

### API 呼び出し
- ヘッダ: `Authorization: Bearer <access_token>`


## 3. TDD 実行

### 1) まとめて実行

```bash
docker compose run --rm \
  -e DJANGO_SETTINGS_MODULE=config.settings.local \
  api pytest -q
```

`--rm` は実行後にコンテナを削除します。  ([Docker Documentation][2])

### 2) 詳細ログで実行

```bash
docker compose run --rm \
  -e DJANGO_SETTINGS_MODULE=config.settings.local \
  api pytest -vv
```

### 3) 失敗したところで止める

```bash
docker compose run --rm \
  -e DJANGO_SETTINGS_MODULE=config.settings.local \
  api pytest -x
```

### 4) 特定テストだけ

```bash
docker compose run --rm \
  -e DJANGO_SETTINGS_MODULE=config.settings.local \
  api pytest -q -k weekly_override
```

## pytest-django（DB/マイグレーション）

pytest-django はテスト用DBを作成して実行します。
繰り返しのテストで速度を上げたい場合は `--reuse-db` が使えます（必要なら `--create-db` で作り直し）。 ([pytest-django Documentation][3])

例:

```bash
docker compose run --rm \
  -e DJANGO_SETTINGS_MODULE=config.settings.local \
  api pytest -q --reuse-db
```

マイグレーションが壊れていると、pytest以前に落ちます（`NodeNotFoundError` など）。

## 4. E2E（curl suite）

- `e2e/suites/local.json` を実行（ローカル）
- `e2e/suites/production.json` を実行（Render本番）

実行例:

```bash
# Docker 内から reverse-proxy を引くのでこれ
export BASE_URL="http://reverse-proxy/api"

docker compose run --rm -T -w /app \
  -e BASE_URL="$BASE_URL" \
  -e ADMIN_JWT="$ADMIN_JWT" \
  -e USER_JWT="$USER_JWT" \
  -e DEVICE_JWT="$DEVICE_JWT" \
  -e DJANGO_SETTINGS_MODULE=config.settings.local \
  -e PYTHONPATH=/app \
  api python e2e/run_curl_suite.py e2e/suites/local.json

```
