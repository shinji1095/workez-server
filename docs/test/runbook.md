# 実行手順（Runbook / TBD）

本Runbookは「コマンド一発」で Unit + Integration + E2E を実行するための想定手順を記載する。
実際のテストランナー（nox/pytest 等）の採用・実装はTBD。

## ローカル実行（想定）
### 例1：noxでまとめて実行（想定）
- 前提：`nox` と `pytest` が導入済み（TBD）
- 実行例：
  - `nox -s unit integration e2e_local`

### 例2：pytest + スクリプトで実行（想定）
- 前提：`pytest` が導入済み（TBD）
- 実行例：
  - `pytest -q tests/unit`
  - `pytest -q tests/integration`
  - `python e2e/run_curl_suite.py --base-url http://127.0.0.1:8000 --suite local`

## デプロイ後実行（想定）
### 例：E2Eのみ実行
- 前提：デプロイ先のURLが確定していること（TBD）
- 実行例：
  - `python e2e/run_curl_suite.py --base-url https://<render-service>.onrender.com --suite prod`

## 実行前提（環境変数・認証準備）
- `BASE_URL`：E2Eの対象URL（例：`http://127.0.0.1:8000`）
- 認証情報（TBD）：
  - JWT/セッション/API Key 等の方式は未確定
  - 認証が必要な場合、`AUTH_TOKEN` や `DEVICE_API_KEY` 等を環境変数で渡す想定（名称はTBD）
- テストデータ規約：
  - 本番DBを汚さない（テストはローカル/検証環境で実施）
  - 書き込み系のE2Eは識別子prefix（例：`e2e_`）等で区別（具体はTBD）

## 失敗時の参照先
- OpenAPI：`docs/api/openapi.yaml`
- 権限表：`docs/auth/permission_matrix.csv`
- 共通エラー形式：`ErrorResponse`（openapi.yaml の components/schemas/ErrorResponse）
