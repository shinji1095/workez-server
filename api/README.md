# Django API Server (Django + DRF)

## 根拠（一次情報）
- `01_WEB機能一覧(機能一覧).csv`
- `openapi.yaml`

本リポジトリは上記2ファイルのエンドポイント（path/method/operationId）を前提に、TDDで実装する構成です。

---

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

---

## 2. 認証（暫定実装）

CSVの「一般≧/管理者≧」をコードで担保するために、OpenAPI未記載の **API Key 認証**を暫定導入しています。

- ヘッダ: `X-API-KEY: <key>` または `Authorization: Bearer <key>`
- ロール:
  - `ADMIN_API_KEY` → admin
  - `USER_API_KEY` → user（一般）
  - `DEVICE_API_KEY` → device

OpenAPI側のsecurity定義は未更新です（意図を崩さないため）。

---

## 3. TDD 実行

### pytest（ユニット＋統合）

```bash
pytest -q
```

### nox（Windowsでも再現しやすい統一実行）

```bash
nox -s unit
nox -s integration
nox -s e2e_local
```

### tools 統合ランナー

```bash
python tools/run_all_tests.py
```

---

## 4. E2E（curl suite）

- `e2e/suites/local.json` を実行（ローカル）
- `e2e/suites/production.json` を実行（Render本番）

実行例:

```bash
export BASE_URL=http://127.0.0.1:8000
export ADMIN_API_KEY=...
python e2e/run_curl_suite.py e2e/suites/local.json
```

---

## 5. OpenAPIに未確定（TBD）の箇所について

`openapi.yaml` の以下は `TBD` になっており、実装で勝手に固定しない方針です。

- 一部の request schema（例: createUsersRequest など）
- 一部のクエリパラメータ（例: harvest category override の対象 period 指定）

このリポジトリでは **暫定の最小ペイロード**で受理できるようにしつつ、
`README.md` に暫定仕様として明示しています。確定後に OpenAPI と実装を同期してください。

暫定仕様:
- 収穫量/不良品 add: device_id, count, occurred_at（任意）を受理
- harvest category override（PATCH）: クエリ `period` を受理（未指定時は当日/当週/当月）

---

## 6. デプロイ（Render）

本番設定:
- `DJANGO_SETTINGS_MODULE=config.settings.production`
- `DATABASE_URL` 必須

依存:
- `requirements/production.txt`

起動コマンド例:
```bash
gunicorn config.wsgi:application
```
