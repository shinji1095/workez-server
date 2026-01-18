# curl コマンド例一覧

このドキュメントは `docs/api/openapi.yaml` に定義されている全エンドポイント（計 35 paths / 45 operations）の curl 実行例です。

## 事前準備

- `BASE_URL` は起動方法に合わせて設定します（末尾スラッシュなし）。
  - Django直（`api` コンテナの 8000 を公開）: `http://localhost:8000`
  - reverse-proxy（nginx）経由（`/api` プレフィックスあり）: `http://localhost/api`
  - ngrok（8000 を公開）: `https://<subdomain>.ngrok-free.app`
  - ngrok（80 を公開 + reverse-proxy 経由）: `https://<subdomain>.ngrok-free.app/api`
  - `BASE_URL="http://localhost:8000/api"` のように `/api` を付けたまま Django 直（8000）を叩くと 404 になり、CSV/PDFとしてエラーレスポンス（JSON等）を保存してしまうので注意してください。
- 認証は原則 JWT（Bearer）です。必要なロールのトークンを用意してください。
  - `ACCESS_TOKEN`: 一般（user）向け
  - `ADMIN_ACCESS_TOKEN`: 管理者（admin）向け
  - `DEVICE_ACCESS_TOKEN`: デバイス（device）向け
- 収穫系のパス変数は環境変数で指定します。
  - `LOT_NAME` / `SIZE_ID` / `RANK_ID` / `HARVEST_DATE`
  - `START_DATE` / `END_DATE`
- `POST /auth/token` は API キー（`X-API-KEY`）で JWT を発行します。
  - `USER_API_KEY` / `ADMIN_API_KEY` / `DEVICE_API_KEY` は `.env.local` 等の値を使います。

例（docker で JWT を作成）:

```sh
# 起動方法に合わせてどちらかを使う（末尾スラッシュなし）
BASE_URL="https://bb248eea47fd.ngrok-free.app"
# BASE_URL="http://localhost/api"

ACCESS_TOKEN="$(docker compose exec -T api python tools/issue_jwt.py --role user --sub user_001)"
ADMIN_ACCESS_TOKEN="$(docker compose exec -T api python tools/issue_jwt.py --role admin --sub admin_001)"

LOT_NAME="1e"
SIZE_ID="S"
RANK_ID="A"
HARVEST_DATE="2025-12-21"
START_DATE="2025-01-01"
END_DATE="2025-01-31"
```

`docker compose` を `-f ...` や `--env-file ...` 付きで起動している場合、`exec` も同じオプションを付けてください。

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
  -d '{"event_id":"550e8400-e29b-41d4-a716-446655440000","count":2.5}'
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

### POST /harvest/amount/add
- 収穫量の送信

```sh
curl -sS -X POST "${BASE_URL}/harvest/amount/add" \
  -H "Authorization: Bearer ${DEVICE_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"event_id":"550e8400-e29b-41d4-a716-446655440000","lot_name":"1e","size_id":"S","rank_id":"A","count":12,"occurred_at":"2025-12-21T12:34:56+09:00"}'
```
### GET /harvest/records/export/csv
- 収穫レコードCSV出力

```sh
curl -sS -f -L -o harvest_records.csv \
  "${BASE_URL}/harvest/records/export/csv?start_date=${START_DATE}&end_date=${END_DATE}&lot=${LOT_NAME}&size=${SIZE_ID}&rank=${RANK_ID}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### GET /harvest/records/report/pdf
- 収穫レポートPDF出力

```sh
curl -sS -f -L -o harvest_report.pdf \
  "${BASE_URL}/harvest/records/report/pdf?start_date=${START_DATE}&end_date=${END_DATE}&lot=${LOT_NAME}&size=${SIZE_ID}&rank=${RANK_ID}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
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
curl -sS "${BASE_URL}/harvest/amount/daily/size/${SIZE_ID}?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### PATCH /harvest/amount/daily/size/{sizeId}
- 仕分けサイズごとの 日間収穫量の変更

```sh
curl -sS -X PATCH "${BASE_URL}/harvest/amount/daily/size/${SIZE_ID}?date=${HARVEST_DATE}" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"count":123}'
```
### GET /harvest/amount/daily/lot/{lotName}
- ロットごとの 日間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/daily/lot/${LOT_NAME}?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### GET /harvest/amount/daily/rank/{rankId}
- 仕分けランクごとの 日間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/daily/rank/${RANK_ID}?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### GET /harvest/amount/daily/size/{sizeId}/rank/{rankId}
- 仕分けランク・サイズごとの 日間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/daily/size/${SIZE_ID}/rank/${RANK_ID}?page=1&page_size=10" \
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
curl -sS "${BASE_URL}/harvest/amount/monthly/size/${SIZE_ID}?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### PATCH /harvest/amount/monthly/size/{sizeId}
- 仕分けサイズごとの 月間収穫量の変更

```sh
curl -sS -X PATCH "${BASE_URL}/harvest/amount/monthly/size/${SIZE_ID}?month=2025-12" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"count":123}'
```
### GET /harvest/amount/monthly/lot/{lotName}
- ロットごとの 月間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/monthly/lot/${LOT_NAME}?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### GET /harvest/amount/monthly/rank/{rankId}
- 仕分けランクごとの 月間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/monthly/rank/${RANK_ID}?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### GET /harvest/amount/monthly/size/{sizeId}/rank/{rankId}
- 仕分けランク・サイズごとの 月間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/monthly/size/${SIZE_ID}/rank/${RANK_ID}?page=1&page_size=10" \
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
curl -sS "${BASE_URL}/harvest/amount/weekly/size/${SIZE_ID}?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### PATCH /harvest/amount/weekly/size/{sizeId}
- 仕分けサイズごとの 週間収穫量の変更

```sh
curl -sS -X PATCH "${BASE_URL}/harvest/amount/weekly/size/${SIZE_ID}?date=${HARVEST_DATE}" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"count":123}'
```
### GET /harvest/amount/weekly/lot/{lotName}
- ロットごとの 週間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/weekly/lot/${LOT_NAME}?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### GET /harvest/amount/weekly/rank/{rankId}
- 仕分けランクごとの 週間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/weekly/rank/${RANK_ID}?page=1&page_size=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### GET /harvest/amount/weekly/size/{sizeId}/rank/{rankId}
- 仕分けランク・サイズごとの 週間収穫量

```sh
curl -sS "${BASE_URL}/harvest/amount/weekly/size/${SIZE_ID}/rank/${RANK_ID}?page=1&page_size=10" \
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
curl -sS -X POST "${BASE_URL}/prices/size/${SIZE_ID}/rank/${RANK_ID}" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"year":2025,"month":12,"unit_price_yen":120}'
```
### PUT /prices/size/{sizeId}/rank/{rankId}
- 単価変更

```sh
curl -sS -X PUT "${BASE_URL}/prices/size/${SIZE_ID}/rank/${RANK_ID}" \
  -H "Authorization: Bearer ${ADMIN_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"year":2025,"month":12,"unit_price_yen":120}'
```
### DELETE /prices/size/{sizeId}/rank/{rankId}
- 単価削除

```sh
curl -sS -X DELETE "${BASE_URL}/prices/size/${SIZE_ID}/rank/${RANK_ID}?year=2025&month=12" \
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
curl -sS -X POST "${BASE_URL}/tablet/harvest/${HARVEST_DATE}?lot=${LOT_NAME}&size=${SIZE_ID}&rank=${RANK_ID}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"count":123}'
```
### GET /tablet/harvest/{date}
- タブレット入力収穫数取得

```sh
curl -sS "${BASE_URL}/tablet/harvest/${HARVEST_DATE}?lot=${LOT_NAME}&size=${SIZE_ID}&rank=${RANK_ID}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
### PUT /tablet/harvest/{date}
- タブレット入力収穫数変更

```sh
curl -sS -X PUT "${BASE_URL}/tablet/harvest/${HARVEST_DATE}?lot=${LOT_NAME}&size=${SIZE_ID}&rank=${RANK_ID}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"count":123}'
```
### DELETE /tablet/harvest/{date}
- タブレット入力収穫数削除

```sh
curl -sS -X DELETE "${BASE_URL}/tablet/harvest/${HARVEST_DATE}?lot=${LOT_NAME}&size=${SIZE_ID}&rank=${RANK_ID}" \
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
