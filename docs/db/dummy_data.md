# 収穫（harvest）ダミーデータ

DB に harvest のダミーレコードを投入/削除する手順です。

## 前提

- docker compose で `api` コンテナが起動していること
- マイグレーションが適用済みであること（`api` サービス起動時に `python manage.py migrate` を実行します）

## ダミーデータ投入

### `seed_harvest_dummy` の引数

| 引数 | 型 | デフォルト | 説明 |
|---|---|---:|---|
| `--days` | int | `30` | 生成する日数（`start-date` から過去にさかのぼって作成） |
| `--per-day` | int | `20` | 1日あたりのレコード数 |
| `--start-date` | date(YYYY-MM-DD) | (当日) | 生成開始日（未指定の場合はサーバーの当日） |
| `--lot-names` | csv | `1a,1b,2e` | 使用するロット名（カンマ区切り） |
| `--size-ids` | csv | `L,M,S` | 使用するサイズID（カンマ区切り） |
| `--rank-ids` | csv | `A,B` | 使用するランクID（カンマ区切り） |
| `--min-count` | decimal(str) | `0.1` | `count` の最小値（`0.1` 刻み） |
| `--max-count` | decimal(str) | `5` | `count` の最大値（`0.1` 刻み） |
| `--event-id-prefix` | hex(str) | `d00d5eed` | ダミー判定用の `event_id` プレフィックス（24桁以下の hex） |
| `--seed` | int | `0` | 乱数シード（同じ値なら同じデータになりやすい） |
| `--batch-size` | int | `500` | `bulk_create` のバッチサイズ |
| `--dry-run` | flag | - | 追加せずに件数だけ表示 |

件数だけ確認（dry-run）:

```sh
docker compose exec api python manage.py seed_harvest_dummy --dry-run
```

投入（デフォルト設定）:

```sh
docker compose exec api python manage.py seed_harvest_dummy
```

デフォルトの仕様:
- `count`: `0.1`〜`5.0` の範囲で `0.1` 刻みのランダム
- `event_id`: 固定の hex プレフィックス（`--event-id-prefix`、デフォルト `d00d5eed`）で生成（ダミー判定に使用）
- `lot_name`: `--lot-names` から選択（デフォルト `1a,1b,2e`）

オプション例:

```sh
docker compose exec api python manage.py seed_harvest_dummy \
  --days 14 \
  --per-day 30 \
  --start-date 2024-01-31 \
  --lot-names 1a,1b,2e,3a \
  --size-ids S,M,L \
  --rank-ids A,B \
  --min-count 0.1 \
  --max-count 5.0 \
  --event-id-prefix d00d5eed
```

## ダミーデータ削除

### `purge_harvest_dummy` の引数

| 引数 | 型 | デフォルト | 説明 |
|---|---|---:|---|
| `--event-id-prefix` | hex(str) | `d00d5eed` | 削除対象にする `event_id` プレフィックス（`seed_harvest_dummy` と同じ値を指定） |
| `--dry-run` | flag | - | 削除せずに件数だけ表示 |

削除対象件数だけ確認（dry-run）:

```sh
docker compose exec api python manage.py purge_harvest_dummy --dry-run
```

削除（同じ `event_id` プレフィックスで削除）:

```sh
docker compose exec api python manage.py purge_harvest_dummy --event-id-prefix d00d5eed
```

## 補足

- `docker-compose.local.yml` を使う場合は、`docker compose` を次に読み替えてください: `docker compose -f docker-compose.local.yml`
