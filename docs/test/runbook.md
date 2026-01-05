# 実行手順（Runbook）

本Runbookは、ローカルで Unit / Integration / System / E2E を実行する手順をまとめる。

## ローカル（pytest）
- 前提：`api/requirements/local.txt` がインストール済み
- 実行（Unit + Integration + System）：
  - `cd api && python3 -m pytest -q`
- 収穫登録（タブレット）システムテストだけ実行：
  - `cd api && python3 -m pytest -q -k system_tablet_harvest_register`

## ローカル（nox）
- 前提：`nox` がインストール済み
- 実行例：
  - `cd api && nox -s unit integration`

## E2E（curl suite）
curlでデプロイ先疎通確認を行う（DBは汚さない想定）。

- 実行例（ローカルサーバに対して）：
  - `cd api && BASE_URL=http://127.0.0.1:8000 python3 e2e/run_curl_suite.py e2e/suites/local.json`

## 認証（JWT）
E2E/curl 実行時は JWT を環境変数で渡す。

- JWT発行（例）：
  - `cd api && DJANGO_SETTINGS_MODULE=config.settings.local python3 tools/issue_jwt.py --role user --sub user_001`
- E2E実行時に設定する代表的な変数：
  - `BASE_URL`（例：`http://127.0.0.1:8000`）
  - `ADMIN_JWT` / `USER_JWT` / `DEVICE_JWT`

## 失敗時の参照先
- OpenAPI：`docs/api/openapi.yaml`
- 共通エラー形式：`api/apps/common/responses.py`
