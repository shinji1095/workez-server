# Raspberry Pi 5 IoT Device

Raspberry Pi 5（Ubuntu 24.04 LTS Server）上で動作する IoT デバイスプログラムです。  
Seeed XIAO nRF52840 を「ADC + センサ読み取りノード」として用い、UART 経由で Raspberry Pi に測距センサ値を送ります。  
Raspberry Pi 側は、物体通過イベントを検知して回数をカウントし、一定間隔で Django サーバへ `/harvest/amount/add` に送信します（JWT 認証）。

---

## 1. システム概要

- センサ：シャープ測距モジュール **GP2Y0A21YK**（アナログ出力）
- ADC：**XIAO nRF52840**（ADC でサンプリングし UART で送信）
- 集計・送信：**Raspberry Pi 5**（通過検知、カウント、10分ごと送信）
- サーバ：Ubuntu PC 上の **Django API**（JWT Bearer 認証）

---

## 2. フォルダ構成

```
device/
  README.md
  requirements.txt
  config/
    config.example.yaml
    config.yaml            # 自分の環境用（作成）
  src/
    workez_device/
      __main__.py
      app.py
      config.py
      detector.py
      serial_reader.py
      sender.py
      state_store.py
      logging_setup.py
  systemd/
    workez-device.service
  log/                     # 起動時刻ファイル名でログ生成
  state/                   # 未送信分カウントなどの永続化
```

---

## 3. 接続図（配線）

### 3.1 センサ（GP2Y0A21YK）→ XIAO nRF52840（ADC）

GP2Y0A21YK は 5V 駆動の距離センサで、出力はアナログ電圧です。XIAO 側で A0 に入力して ADC で読み取ります。

```
[GP2Y0A21YK]                 [XIAO nRF52840]
  VCC   --------------------   5V（外部5V電源）
  GND   --------------------   GND  （共通GND）
  Vout  --------------------   A0（D0）※アナログ入力

  推奨：VCC-GND 間に 10µF 以上のコンデンサ（センサ近傍）
```

注意：
- XIAO の ADC 入力は 3.3V 系です。GP2Y0A21YK の Vout が 3.3V を超えないことを実測で確認してください。
- 5V は Raspberry Pi の 5V ピン（高電流供給）から取る場合でも、GND を必ず共通化してください。

---

### 3.2 XIAO → Raspberry Pi 5（UART）

XIAO の UART は **Serial1（TX=D6, RX=D7）** を使います。  
Raspberry Pi の UART は 3.3V ロジックです（XIAO と同電圧）。

#### A) Raspberry Pi の GPIO UART に直結する場合（推奨）

```
[XIAO nRF52840]                 [Raspberry Pi 5 40pin]
  D6 (TX / Serial1 TX)  ------  RXD0 (GPIO15, Pin 10)
  D7 (RX / Serial1 RX)  ------  TXD0 (GPIO14, Pin 8)   ※双方向通信する場合
  GND                   ------  GND (Pin 6 など)
```

#### B) USB-UART 変換器を使う場合（運用が簡単）

```
[XIAO D6(TX)] -> [USB-UART RX]
[XIAO D7(RX)] -> [USB-UART TX]  ※双方向の場合
[GND 共通]     -> [USB-UART GND]
USB-UART を Raspberry Pi に挿す（例：/dev/ttyUSB0）
```

---

## 4. XIAO（Arduino IDE）側：UART 出力フォーマット

Raspberry Pi 側は、XIAO から **1行1JSON（NDJSON）** でデータが届くことを想定しています。

例（改行で区切る）：
```json
{"ts_ms": 123456, "voltage_mv": 1520, "raw": 1887}
```

- `ts_ms`：XIAO 起動後の経過ミリ秒（`millis()`）
- `voltage_mv`：ADC 値を mV 換算した値（必須）
- `raw`：ADC 生値（任意、デバッグ用）

---

## 5. Raspberry Pi 側セットアップ（Ubuntu 24.04 LTS Server）

### 5.1 Python 環境の作成

```bash
cd ~/device
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
cp config/config.example.yaml config/config.yaml
```

### 5.2 設定（config.yaml）

最低限ここを環境に合わせて編集します：

- `server.base_url`：Django サーバのベースURL
- `server.jwt.token`：デバイス用 JWT（Bearer、固定運用の場合）
- `server.jwt.token_url`：トークン発行URL（例：`http://<host>:8000/auth/token`）
- `server.jwt.api_key`：デバイス用 API キー（X-API-KEY）
- `server.jwt.sub`：JWT の subject（未指定なら `device.device_id` を使用）
- `serial.port`：UART デバイス（例：`/dev/ttyAMA0` or `/dev/serial0` or `/dev/ttyUSB0`）
- `device.device_id` / `device.category_id`
- `sender.send_interval_s`：送信間隔（デフォルト 600 = 10分）
- `detector.threshold_on_mv` / `detector.threshold_off_mv`：通過判定の閾値（後述）

---

## 6. 通過検知アルゴリズム（Pi側）

`src/workez_device/detector.py` の `PassDetector` が、以下の考え方で通過イベントを検知します。

- EMA（指数移動平均）で平滑化
- ON/OFF のヒステリシス（`threshold_on_mv` / `threshold_off_mv`）でチャタリング抑制
- 連続サンプル数（`consecutive_on/off`）でノイズ除去
- 物体は 0.5s 以上の間隔で 1個ずつ通過する前提のため、`min_gap_s` で二重カウント抑制

調整のコツ：
1. まず `--debug` で起動し、通過時の `voltage_mv` のレンジを確認
2. 物体が「いる」時に超える値を `threshold_on_mv`
3. 物体が「いない」時に下回る値を `threshold_off_mv`（ON より十分低く）

---

## 7. 実行方法

### 7.1 手動起動（デバッグ）

```bash
source .venv/bin/activate
python -m workez_device --config config/config.yaml --debug
```

- `log/<起動時刻>.log` にログが出ます
- `--debug` でコンソールにも INFO ログを出します

### 7.2 systemd で自動起動（電源ONで起動）

```bash
sudo cp systemd/workez-device.service /etc/systemd/system/workez-device.service
sudo systemctl daemon-reload
sudo systemctl enable workez-device
sudo systemctl start workez-device
sudo systemctl status workez-device --no-pager
```

ログ確認：
```bash
journalctl -u workez-device -f
```

---

## 8. Raspberry Pi の UART 有効化（GPIO直結の場合）

環境によって手順が異なるため、ここは「確認ポイント」のみ記載します。

1. `/dev/serial0` が存在するか
   ```bash
   ls -l /dev/serial0
   ```
2. `/boot/firmware/config.txt` に `enable_uart=1` が必要な場合があります  
3. シリアルコンソール（ログインコンソール）と競合している場合は無効化します  
   - 例：`systemctl status serial-getty@ttyAMA0.service` 等で確認

※どの UART デバイス名になるか（`/dev/ttyAMA0`、`/dev/ttyS0`、`/dev/serial0`）は、OS/設定により変わります。`config.yaml` の `serial.port` を実際のデバイス名に合わせてください。

---

## 9. サーバ送信について

Pi 側は一定間隔ごとに、未送信のカウントをまとめて `/harvest/amount/add` に送信します。  
送信に失敗した場合は、未送信分を `state/state.json` に保持し、次回再送します。

---

## 10. トラブルシュート

### 10.1 受信がない（Pi側）
- `serial.port` が正しいか（USB-UART なら `/dev/ttyUSB0` など）
- ボーレートが一致しているか（デフォルト 115200）
- GND が共通になっているか
- TX/RX が交差になっているか（TX→RX）

### 10.2 通過が二重カウントされる
- `detector.min_gap_s` を増やす（例：0.6〜0.8）
- `threshold_on/off` の間隔を広げる（ヒステリシスを強くする）
- `consecutive_on/off` を増やす

### 10.3 全く検知しない
- `threshold_on_mv` を下げてレンジ確認
- センサの距離レンジ（10〜80cm）内で測れているか
- センサの電源（5V）と GND 共通を確認

---

## 参考（主要資料）

- SHARP. "GP2Y0A21YK0F Distance Measuring Sensor Unit Datasheet". （PDF） (accessed 2025-12-24).
- Seeed Studio Wiki. "XIAO nRF52840 / Sense". (accessed 2025-12-24).
