# データベース定義

## 1. スコープ
- 本資料は Django アプリが管理する業務テーブルを対象とする（`auth_*`, `django_*` などの Django 標準テーブルは省略）。
- 本資料は以下の変更を反映する：
  - `defects_records` から `device_id` を削除
  - `harvest_records` から `device_id` / `category_id` / `category_name` を削除し、`size_id` / `rank_id` / `lot_name` を追加
  - `harvest_aggregate_overrides` の `category_id` / `category_name` を `size_id` / `size_name` に変更
  - `price_records` から `category_id` / `category_name` を削除し、`size_id` / `rank_id` を追加
  - `sizes` / `ranks` テーブルを追加（初期レコードあり）

## 2. DBエンジン（環境差分）
- 開発（デフォルト）：SQLite3（`api/db.sqlite3`）
- `DATABASE_URL` が設定されている場合：その設定に従う（例：PostgreSQL）

補足：
- `USE_TZ=True` のため、`DateTimeField` はタイムゾーン付きとして扱う（DBへの保存形式はエンジンに依存）。

## 3. リレーション（物理FKのみ）
```mermaid
erDiagram
  devices ||--|| device_battery_status : "1:1"
  devices ||--o{ device_alarms : "1:N"
  sizes ||--o{ harvest_records : "1:N"
  sizes ||--o{ harvest_aggregate_overrides : "1:N"
  ranks ||--o{ harvest_records : "1:N"
  sizes ||--o{ price_records : "1:N"
  ranks ||--o{ price_records : "1:N"
```

## 4. テーブル定義

### `app_users`（`apps.users.User`）
| カラム | 型（概念） | NULL | 制約/補足 |
|---|---|---:|---|
| `id` | uuid | NO | PK |
| `email` | varchar(254) | NO | UNIQUE |
| `name` | varchar(255) | NO |  |
| `role` | varchar(20) | NO | default=`user`（`admin`/`user`） |
| `is_active` | boolean | NO | default=`true` |
| `created_at` | datetime | NO | 自動設定（作成時） |
| `updated_at` | datetime | NO | 自動更新 |

### `devices`（`apps.devices.Device`）
| カラム | 型（概念） | NULL | 制約/補足 |
|---|---|---:|---|
| `id` | varchar(64) | NO | PK |
| `name` | varchar(255) | NO |  |
| `status` | varchar(32) | NO | default=`active`（`active`/`inactive`/`maintenance`） |
| `created_at` | datetime | NO | 自動設定（作成時） |
| `updated_at` | datetime | NO | 自動更新 |

### `device_battery_status`（`apps.devices.BatteryStatus`）
| カラム | 型（概念） | NULL | 制約/補足 |
|---|---|---:|---|
| `id` | bigint | NO | PK（自動採番） |
| `device_id` | varchar(64) | NO | UNIQUE、FK → `devices.id`（`ON DELETE CASCADE`） |
| `percent` | int | NO |  |
| `voltage_mv` | int | YES |  |
| `is_charging` | boolean | NO | default=`false` |
| `updated_at` | datetime | NO | 自動更新 |

### `device_alarms`（`apps.devices.Alarm`）
| カラム | 型（概念） | NULL | 制約/補足 |
|---|---|---:|---|
| `alarm_id` | uuid | NO | PK |
| `device_id` | varchar(64) | NO | FK → `devices.id`（`ON DELETE CASCADE`） |
| `type` | varchar(32) | NO | `battery_low`/`sensor_failure`/`network_error` |
| `message` | text | NO |  |
| `status` | varchar(32) | NO | default=`open`（`open`/`acknowledged`/`closed`） |
| `severity` | varchar(16) | YES | `info`/`warning`/`critical` |
| `occurred_at` | datetime | NO |  |
| `created_at` | datetime | NO | 自動設定（作成時） |

### `harvest_records`（`apps.harvest.HarvestRecord`）
| カラム | 型（概念） | NULL | 制約/補足 |
|---|---|---:|---|
| `id` | uuid | NO | PK |
| `event_id` | uuid | YES | UNIQUE（冪等キー用途） |
| `lot_name` | varchar(64) | NO |  |
| `size_id` | varchar(64) | NO | FK → `sizes.size_id` |
| `rank_id` | varchar(64) | NO | FK → `ranks.rank_id` |
| `count` | int | NO | 収穫量（g） |
| `occurred_at` | datetime | NO |  |
| `created_at` | datetime | NO | 自動設定（作成時） |

### `harvest_aggregate_overrides`（`apps.harvest.HarvestAggregateOverride`）
| カラム | 型（概念） | NULL | 制約/補足 |
|---|---|---:|---|
| `id` | uuid | NO | PK |
| `period_type` | varchar(16) | NO | `daily`/`weekly`/`monthly` |
| `period` | varchar(16) | NO | `YYYY-MM-DD` / `YYYY-Www` / `YYYY-MM` |
| `size_id` | varchar(64) | NO | FK → `sizes.size_id` |
| `size_name` | varchar(255) | YES |  |
| `total_count` | int | NO |  |
| `updated_at` | datetime | NO | 自動更新 |

制約：
- UNIQUE（`period_type`, `period`, `size_id`）

### `harvest_targets`（`apps.harvest.HarvestTarget`）
| カラム | 型（概念） | NULL | 制約/補足 |
|---|---|---:|---|
| `id` | uuid | NO | PK |
| `target_type` | varchar(16) | NO | UNIQUE（`daily`/`weekly`/`monthly`） |
| `target_count` | int | NO |  |
| `updated_at` | datetime | NO | 自動更新 |

### `defects_records`（`apps.defects.DefectsRecord`）
| カラム | 型（概念） | NULL | 制約/補足 |
|---|---|---:|---|
| `id` | uuid | NO | PK |
| `event_id` | uuid | YES | UNIQUE（冪等キー用途） |
| `category_id` | varchar(64) | YES |  |
| `count` | int | NO |  |
| `occurred_at` | datetime | NO |  |
| `created_at` | datetime | NO | 自動設定（作成時） |

### `price_records`（`apps.prices.PriceRecord`）
| カラム | 型（概念） | NULL | 制約/補足 |
|---|---|---:|---|
| `id` | uuid | NO | PK |
| `size_id` | varchar(64) | NO | FK → `sizes.size_id` |
| `rank_id` | varchar(64) | NO | FK → `ranks.rank_id` |
| `unit_price_yen` | int | NO |  |
| `effective_from` | date | NO |  |
| `effective_to` | date | YES |  |
| `updated_at` | datetime | NO | 自動更新 |

制約：
- UNIQUE（`size_id`, `rank_id`, `effective_from`）

### `sizes`（マスタ：サイズ）
| カラム | 型（概念） | NULL | 制約/補足 |
|---|---|---:|---|
| `size_id` | varchar(64) | NO | PK |
| `size_name` | varchar(255) | NO |  |

初期レコード：
- `L`, `M`, `S`, `SS`, `3S`, `小`（= 極小）, `黒`

### `ranks`（マスタ：ランク）
| カラム | 型（概念） | NULL | 制約/補足 |
|---|---|---:|---|
| `rank_id` | varchar(64) | NO | PK |
| `rank_name` | varchar(255) | NO |  |

初期レコード：
- `A`, `B`, `C`, `小`, `廃棄`
