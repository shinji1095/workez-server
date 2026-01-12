# curl コマンド例一覧

このドキュメントは `docs/api/openapi.yaml` に定義されている全エンドポイント（計 37 paths / 50 operations）の curl 実行例です。

## 事前準備

- `BASE_URL` は起動方法に合わせて設定します（末尾スラッシュなし）。
  - Django直: `http://localhost:8000`
  - reverse-proxy（nginx）経由: `http://localhost/api`
- 認証は原則 JWT（Bearer）です。必要なロールのトークンを用意してください。
  - `ACCESS_TOKEN`: 一般（user）向け
  - `ADMIN_ACCESS_TOKEN`: 管理者（admin）向け
- `POST /auth/token` は API キー（`X-API-KEY`）で JWT を発行します。
  - `USER_API_KEY` / `ADMIN_API_KEY` / `DEVICE_API_KEY` は `.env.local` 等の値を使います。

例（ローカル開発用: `tools/issue_jwt.py` でJWTを作成）:

```sh
ACCESS_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyXzAwMSIsInJvbGUiOiJ1c2VyIiwiaWF0IjoxNzY4MTgwNjc2LCJleHAiOjE3NjgxODQyNzZ9.pop8pd_yky84Db9hjfxtFA1WBrz3ApSVAFyhBTxL-zM
ADMIN_ACCESS_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbl8wMDEiLCJyb2xlIjoiYWRtaW4iLCJpYXQiOjE3NjgxODA3MjUsImV4cCI6MTc2ODE4NDMyNX0.x1fEQLgbdU4xLkJ_qJ7x0n_YRk8Id1S2WALpjFpGLxE
BASE_URL="https://bb248eea47fd.ngrok-free.app/"
```

## エンドポイント別 curl 例

### PUT /admin/users/{userId}
- 管理ユーザー権限変更

```sh
curl -sS -X PUT "${BASE_URL}/admin/users/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"name":"山田太郎","role":"user","is_active":true}'
```
### POST /auth/token
- トークン発行

```sh
curl -sS -X POST "${BASE_URL}/auth/token" \
  -H "X-API-KEY: ${USER_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"sub":"user-1"}'
```
### GET /analytics/harvest/monthly
- 月間収穫量予想

```sh
curl -sS "${BASE_URL}/analytics/harvest/monthly?page=1&page_size=10" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}"
```
### GET /analytics/revenue/monthly
- 月間売上

```sh
curl -sS "${BASE_URL}/analytics/revenue/monthly?page=1&page_size=10" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}"
```
### GET /analytics/revenue/yearly
- 年間売り上げ

```sh
curl -sS "${BASE_URL}/analytics/revenue/yearly?page=1&page_size=10" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}"
```
### POST /defects/amount/add
- 不良品数の送信

```sh
curl -sS -X POST "${BASE_URL}/defects/amount/add" \
  -H "Authorization: Bearer ${DEVICE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"event_id":"550e8400-e29b-41d4-a716-446655440000","category_id":"S","count":12,"occurred_at":"2025-12-21T12:34:56+09:00"}'
```
### GET /defects/amount/monthly
- 月間不良品数

```sh
curl -sS "${BASE_URL}/defects/amount/monthly?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### GET /defects/amount/weekly
- 週間不良品数

```sh
curl -sS "${BASE_URL}/defects/amount/weekly?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### GET /defects/ratio/monthly
- 月間不良品割合

```sh
curl -sS "${BASE_URL}/defects/ratio/monthly?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### GET /defects/ratio/weekly
- 週間不良品割合

```sh
curl -sS "${BASE_URL}/defects/ratio/weekly?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### GET /devices/{deviceId}/alarm
- 故障アラーム

```sh
curl -sS "${BASE_URL}/devices/DEV001/alarm" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### POST /devices/{deviceId}/alarm
- 故障アラーム通知

```sh
curl -sS -X POST "${BASE_URL}/devices/DEV001/alarm" \
  -H "Authorization: Bearer ${DEVICE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"alarm_id":"550e8400-e29b-41d4-a716-446655440000","type":"battery_low","message":"バッテリー残量が低下しました","status":"open","occurred_at":"2025-12-15T12:34:56+09:00"}'
```
### GET /devices/{deviceId}/alarm/detail
- 故障アラーム（詳細）

```sh
curl -sS "${BASE_URL}/devices/DEV001/alarm/detail?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### GET /devices/{deviceId}/battery
- バッテリー監視

```sh
curl -sS "${BASE_URL}/devices/DEV001/battery" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### POST /devices/{deviceId}/battery
- バッテリー状態送信

```sh
curl -sS -X POST "${BASE_URL}/devices/DEV001/battery" \
  -H "Authorization: Bearer ${DEVICE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"percent":80,"is_charging":false,"updated_at":"2025-12-21T12:34:56+09:00"}'
```
### POST /harvest/amount/add
- 収穫量の送信

```sh
curl -sS -X POST "${BASE_URL}/harvest/amount/add" \
  -H "Authorization: Bearer ${DEVICE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"event_id":"550e8400-e29b-41d4-a716-446655440000","lot_name":"1e","size_id":"S","rank_id":"A","count":12,"occurred_at":"2025-12-21T12:34:56+09:00"}'
```
### GET /harvest/amount/daily
- 日間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/daily?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### GET /harvest/amount/daily/size/{sizeId}
- 仕分けサイズごとの 日間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/daily/size/S?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### PATCH /harvest/amount/daily/size/{sizeId}
- 仕分けサイズごとの 日間収穫量の変更

```sh
curl -sS -X PATCH "${BASE_URL}/harvest/amount/daily/size/S?date=2025-12-21" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"count":123}'
```
### GET /harvest/amount/daily/rank/{rankId}
- 仕分けランクごとの 日間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/daily/rank/A?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### GET /harvest/amount/daily/size/{sizeId}/rank/{rankId}
- 仕分けランク・サイズごとの 日間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/daily/size/S/rank/A?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### GET /harvest/amount/monthly
- 月間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/monthly?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### GET /harvest/amount/monthly/size/{sizeId}
- 仕分けサイズごとの 月間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/monthly/size/S?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### PATCH /harvest/amount/monthly/size/{sizeId}
- 仕分けサイズごとの 月間収穫量の変更

```sh
curl -sS -X PATCH "${BASE_URL}/harvest/amount/monthly/size/S?month=2025-12" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"count":123}'
```
### GET /harvest/amount/monthly/rank/{rankId}
- 仕分けランクごとの 月間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/monthly/rank/A?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### GET /harvest/amount/monthly/size/{sizeId}/rank/{rankId}
- 仕分けランク・サイズごとの 月間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/monthly/size/S/rank/A?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### GET /harvest/amount/weekly
- 週間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/weekly?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### GET /harvest/amount/weekly/size/{sizeId}
- 仕分けサイズごとの 週間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/weekly/size/S?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### PATCH /harvest/amount/weekly/size/{sizeId}
- 仕分けサイズごとの 週間収穫量の変更

```sh
curl -sS -X PATCH "${BASE_URL}/harvest/amount/weekly/size/S?date=2025-12-21" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"count":123}'
```

### GET /harvest/amount/weekly/rank/{rankId}
- 仕分けランクごとの 週間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/weekly/rank/A?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### GET /harvest/amount/weekly/size/{sizeId}/rank/{rankId}
- 仕分けランク・サイズごとの 週間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/weekly/size/S/rank/A?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### PUT /harvest/target/daily
- 1日目標収穫量設定

```sh
curl -sS -X PUT "${BASE_URL}/harvest/target/daily" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"target_count":4000}'
```
### PUT /harvest/target/monthly
- 月間目標収穫量設定

```sh
curl -sS -X PUT "${BASE_URL}/harvest/target/monthly" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"target_count":4000}'
```
### PUT /harvest/target/weekly
- 週間目標収穫量設定

```sh
curl -sS -X PUT "${BASE_URL}/harvest/target/weekly" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"target_count":4000}'
```
### POST /prices/size/{sizeId}/rank/{rankId}
- 単価登録

```sh
curl -sS -X POST "${BASE_URL}/prices/size/S/rank/A" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"year":2025,"month":12,"unit_price_yen":120}'
```
### PUT /prices/size/{sizeId}/rank/{rankId}
- 単価変更

```sh
curl -sS -X PUT "${BASE_URL}/prices/size/S/rank/A" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"year":2025,"month":12,"unit_price_yen":120}'
```
### DELETE /prices/size/{sizeId}/rank/{rankId}
- 単価削除

```sh
curl -sS -X DELETE "${BASE_URL}/prices/size/S/rank/A?year=2025&month=12" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}"
```

### GET /prices/monthly
- 単価一覧（月間）

```sh
curl -sS "${BASE_URL}/prices/monthly?page=1&page_size=10" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}"
```
### GET /prices/yearly
- 単価一覧（年間）

```sh
curl -sS "${BASE_URL}/prices/yearly?page=1&page_size=10" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}"
```
### POST /tablet/harvest/{date}
- タブレット入力収穫数追加

```sh
curl -sS -X POST "${BASE_URL}/tablet/harvest/2025-12-21?lot=1e&size=S&rank=A" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"count":123}'
```
### GET /tablet/harvest/{date}
- タブレット入力収穫数取得

```sh
curl -sS "${BASE_URL}/tablet/harvest/2025-12-21?lot=1e&size=S&rank=A" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### PUT /tablet/harvest/{date}
- タブレット入力収穫数変更

```sh
curl -sS -X PUT "${BASE_URL}/tablet/harvest/2025-12-21?lot=1e&size=S&rank=A" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"count":123}'
```
### DELETE /tablet/harvest/{date}
- タブレット入力収穫数削除

```sh
curl -sS -X DELETE "${BASE_URL}/tablet/harvest/2025-12-21?lot=1e&size=S&rank=A" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### GET /users
- ユーザー一覧

```sh
curl -sS "${BASE_URL}/users?page=1&page_size=10" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}"
```
### POST /users
- ユーザー登録

```sh
curl -sS -X POST "${BASE_URL}/users" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","name":"山田太郎","password":"password1234"}'
```

### PATCH /users/{userId}
- ユーザー変更

```sh
curl -sS -X PATCH "${BASE_URL}/users/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"name":"山田花子"}'
```
### DELETE /users/{userId}
- ユーザー削除

```sh
curl -sS -X DELETE "${BASE_URL}/users/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}"
```
