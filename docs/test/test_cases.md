# テストケース一覧（TBD）

## TC-001
- 対象operationId: `createDefectsAmountAdd`
- 対象: 不良品数の送信（POST /defects/amount/add）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 書き込み系のため、実行環境はローカル/検証環境を推奨（本番書き込みは原則禁止、TBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - POST /defects/amount/add にリクエストを送信する
  - requestBodyはCSVに定義が無いため、まずは空JSON {} で試行し、実装仕様に合わせて調整（TBD）
- 期待結果
  - ステータスコードが 201 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-002
- 対象operationId: `createDevices`
- 対象: デバイス登録（POST /devices）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 書き込み系のため、実行環境はローカル/検証環境を推奨（本番書き込みは原則禁止、TBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - POST /devices にリクエストを送信する
  - requestBodyはCSVに定義が無いため、まずは空JSON {} で試行し、実装仕様に合わせて調整（TBD）
- 期待結果
  - ステータスコードが 201 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-003
- 対象operationId: `createDevicesAlerm`
- 対象: 故障アラーム送信（POST /devices/{deviceId}/alerm）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 書き込み系のため、実行環境はローカル/検証環境を推奨（本番書き込みは原則禁止、TBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - POST /devices/{deviceId}/alerm にリクエストを送信する
  - requestBodyはCSVに定義が無いため、まずは空JSON {} で試行し、実装仕様に合わせて調整（TBD）
- 期待結果
  - ステータスコードが 201 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-004
- 対象operationId: `createDevicesBattery`
- 対象: バッテリー状態送信（POST /devices/{deviceId}/battery）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 書き込み系のため、実行環境はローカル/検証環境を推奨（本番書き込みは原則禁止、TBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - POST /devices/{deviceId}/battery にリクエストを送信する
  - requestBodyはCSVに定義が無いため、まずは空JSON {} で試行し、実装仕様に合わせて調整（TBD）
- 期待結果
  - ステータスコードが 201 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-005
- 対象operationId: `createHarvestAmountAdd`
- 対象: 収穫量の送信（POST /harvest/amount/add）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 書き込み系のため、実行環境はローカル/検証環境を推奨（本番書き込みは原則禁止、TBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - POST /harvest/amount/add にリクエストを送信する
  - requestBodyはCSVに定義が無いため、まずは空JSON {} で試行し、実装仕様に合わせて調整（TBD）
- 期待結果
  - ステータスコードが 201 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-006
- 対象operationId: `createPricesCategory`
- 対象: 単価登録（POST /prices/category/{categoryId}）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 書き込み系のため、実行環境はローカル/検証環境を推奨（本番書き込みは原則禁止、TBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - POST /prices/category/{categoryId} にリクエストを送信する
  - requestBodyはCSVに定義が無いため、まずは空JSON {} で試行し、実装仕様に合わせて調整（TBD）
- 期待結果
  - ステータスコードが 201 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-007
- 対象operationId: `createUsers`
- 対象: ユーザー登録（POST /users）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 書き込み系のため、実行環境はローカル/検証環境を推奨（本番書き込みは原則禁止、TBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - POST /users にリクエストを送信する
  - requestBodyはCSVに定義が無いため、まずは空JSON {} で試行し、実装仕様に合わせて調整（TBD）
- 期待結果
  - ステータスコードが 201 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-008
- 対象operationId: `deleteDevices`
- 対象: デバイス削除（DELETE /devices/{deviceId}）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 書き込み系のため、実行環境はローカル/検証環境を推奨（本番書き込みは原則禁止、TBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - DELETE /devices/{deviceId} にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-009
- 対象operationId: `deletePricesCategory`
- 対象: 単価削除（DELETE /prices/category/{categoryId}）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 書き込み系のため、実行環境はローカル/検証環境を推奨（本番書き込みは原則禁止、TBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - DELETE /prices/category/{categoryId} にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-010
- 対象operationId: `deleteUsers`
- 対象: ユーザー削除（DELETE /users/{userId}）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 書き込み系のため、実行環境はローカル/検証環境を推奨（本番書き込みは原則禁止、TBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - DELETE /users/{userId} にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-011
- 対象operationId: `listAnalyticsHarvestMonthly`
- 対象: 月間収穫量予想（GET /analytics/harvest/monthly）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /analytics/harvest/monthly にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-012
- 対象operationId: `listAnalyticsRevenueMonthly`
- 対象: 月間売上（GET /analytics/revenue/monthly）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /analytics/revenue/monthly にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-013
- 対象operationId: `listAnalyticsRevenueYealy`
- 対象: 年間売り上げ（GET /analytics/revenue/yealy）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /analytics/revenue/yealy にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-014
- 対象operationId: `listDefectsAmountMonthly`
- 対象: 月間不良品数（GET /defects/amount/monthly）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /defects/amount/monthly にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-015
- 対象operationId: `listDefectsAmountWeekly`
- 対象: 週間不良品数（GET /defects/amount/weekly）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /defects/amount/weekly にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-016
- 対象operationId: `listDefectsRatioMonthly`
- 対象: 月間不良品割合（GET /defects/ratio/monthly）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /defects/ratio/monthly にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-017
- 対象operationId: `listDefectsRatioWeekly`
- 対象: 週間不良品割合（GET /defects/ratio/weekly）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /defects/ratio/weekly にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-018
- 対象operationId: `listDevices`
- 対象: デバイス一覧（GET /devices）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /devices にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-019
- 対象operationId: `listHarvestAmountDaily`
- 対象: 日間収穫量（GET /harvest/amount/daily）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /harvest/amount/daily にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-020
- 対象operationId: `listHarvestAmountMonthly`
- 対象: 月間収穫量（GET /harvest/amount/monthly）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /harvest/amount/monthly にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-021
- 対象operationId: `listHarvestAmountWeekly`
- 対象: 週間収穫量（GET /harvest/amount/weekly）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /harvest/amount/weekly にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-022
- 対象operationId: `listPricesMonthly`
- 対象: 単価一覧（月間）（GET /prices/monthly）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /prices/monthly にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-023
- 対象operationId: `listPricesYearly`
- 対象: 単価一覧（年間）（GET /prices/yearly）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /prices/yearly にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-024
- 対象operationId: `listUsers`
- 対象: ユーザー一覧（GET /users）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /users にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-025
- 対象operationId: `partialUpdateHarvestAmountDailyCategory`
- 対象: 仕分けサイズごとの 日間収穫量の変更（PATCH /harvest/amount/daily/category/{categoryId}）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 書き込み系のため、実行環境はローカル/検証環境を推奨（本番書き込みは原則禁止、TBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - PATCH /harvest/amount/daily/category/{categoryId} にリクエストを送信する
  - requestBodyはCSVに定義が無いため、まずは空JSON {} で試行し、実装仕様に合わせて調整（TBD）
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-026
- 対象operationId: `partialUpdateHarvestAmountMonthlyCategory`
- 対象: 仕分けサイズごとの 月間収穫量の変更（PATCH /harvest/amount/monthly/category/{categoryId}）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 書き込み系のため、実行環境はローカル/検証環境を推奨（本番書き込みは原則禁止、TBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - PATCH /harvest/amount/monthly/category/{categoryId} にリクエストを送信する
  - requestBodyはCSVに定義が無いため、まずは空JSON {} で試行し、実装仕様に合わせて調整（TBD）
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-027
- 対象operationId: `partialUpdateHarvestAmountWeeklyCategory`
- 対象: 仕分けサイズごとの 週間収穫量の変更（PATCH /harvest/amount/weekly/category/{categoryId}）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 書き込み系のため、実行環境はローカル/検証環境を推奨（本番書き込みは原則禁止、TBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - PATCH /harvest/amount/weekly/category/{categoryId} にリクエストを送信する
  - requestBodyはCSVに定義が無いため、まずは空JSON {} で試行し、実装仕様に合わせて調整（TBD）
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-028
- 対象operationId: `partialUpdateUsers`
- 対象: ユーザー変更（PATCH /users/{userId}）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 書き込み系のため、実行環境はローカル/検証環境を推奨（本番書き込みは原則禁止、TBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - PATCH /users/{userId} にリクエストを送信する
  - requestBodyはCSVに定義が無いため、まずは空JSON {} で試行し、実装仕様に合わせて調整（TBD）
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-029
- 対象operationId: `retrieveDevicesAlerm`
- 対象: 故障アラーム（GET /devices/{deviceId}/alerm）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /devices/{deviceId}/alerm にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-030
- 対象operationId: `retrieveDevicesAlermDetail`
- 対象: 故障アラーム（詳細）（GET /devices/{deviceId}/alerm/detail）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /devices/{deviceId}/alerm/detail にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-031
- 対象operationId: `retrieveDevicesBattery`
- 対象: バッテリー監視（GET /devices/{deviceId}/battery）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /devices/{deviceId}/battery にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-032
- 対象operationId: `retrieveHarvestAmountDailyCategory`
- 対象: 仕分けサイズごとの 日間収穫量（GET /harvest/amount/daily/category/{categoryId}）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /harvest/amount/daily/category/{categoryId} にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-033
- 対象operationId: `retrieveHarvestAmountMonthlyCategory`
- 対象: 仕分けサイズごとの 月間収穫量（GET /harvest/amount/monthly/category/{categoryId}）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /harvest/amount/monthly/category/{categoryId} にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-034
- 対象operationId: `retrieveHarvestAmountWeeklyCategory`
- 対象: 仕分けサイズごとの 週間収穫量（GET /harvest/amount/weekly/category/{categoryId}）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - GET /harvest/amount/weekly/category/{categoryId} にリクエストを送信する
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-035
- 対象operationId: `updateAdminUsers`
- 対象: 管理ユーザー権限変更（PUT /admin/users/{userId}）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 書き込み系のため、実行環境はローカル/検証環境を推奨（本番書き込みは原則禁止、TBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - PUT /admin/users/{userId} にリクエストを送信する
  - requestBodyはCSVに定義が無いため、まずは空JSON {} で試行し、実装仕様に合わせて調整（TBD）
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-036
- 対象operationId: `updateHarvestTargetDaily`
- 対象: 1日目標収穫量設定（PUT /harvest/target/daily）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 書き込み系のため、実行環境はローカル/検証環境を推奨（本番書き込みは原則禁止、TBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - PUT /harvest/target/daily にリクエストを送信する
  - requestBodyはCSVに定義が無いため、まずは空JSON {} で試行し、実装仕様に合わせて調整（TBD）
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-037
- 対象operationId: `updateHarvestTargetMonthly`
- 対象: 月間目標収穫量設定（PUT /harvest/target/monthly）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 書き込み系のため、実行環境はローカル/検証環境を推奨（本番書き込みは原則禁止、TBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - PUT /harvest/target/monthly にリクエストを送信する
  - requestBodyはCSVに定義が無いため、まずは空JSON {} で試行し、実装仕様に合わせて調整（TBD）
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-038
- 対象operationId: `updateHarvestTargetWeekly`
- 対象: 週間目標収穫量設定（PUT /harvest/target/weekly）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 書き込み系のため、実行環境はローカル/検証環境を推奨（本番書き込みは原則禁止、TBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - PUT /harvest/target/weekly にリクエストを送信する
  - requestBodyはCSVに定義が無いため、まずは空JSON {} で試行し、実装仕様に合わせて調整（TBD）
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-039
- 対象operationId: `updatePricesCategory`
- 対象: 単価変更（PUT /prices/category/{categoryId}）
- 前提
  - 対象APIが起動していること（BASE_URLはTBD）
  - 書き込み系のため、実行環境はローカル/検証環境を推奨（本番書き込みは原則禁止、TBD）
  - 認証の要否・方式はTBD（必要な場合のトークン/キー準備はTBD）
- 手順
  - PUT /prices/category/{categoryId} にリクエストを送信する
  - requestBodyはCSVに定義が無いため、まずは空JSON {} で試行し、実装仕様に合わせて調整（TBD）
- 期待結果
  - ステータスコードが 200 であること
  - レスポンスがJSONであること
  - レスポンス形式はTBD（フィールド断定不可）
- 異常系（境界値、必須欠落、二重送信）
  - 必須パラメータ欠落（パスパラメータ等）: 400 または 404（実装次第、TBD）
  - 認証が必要な場合: 401/403（実装次第、TBD）
  - 存在しないID指定（{userId}/{deviceId}/{categoryId}）: 404（実装次第、TBD）
  - サーバーエラー時: 500 かつ ErrorResponse 形式

## TC-040
- 対象operationId: `createTabletHarvest`
- 対象: 収穫登録（タブレット）（`harvest_register.html` → POST /tablet/harvest/{date}）
- 前提
  - 対象APIが起動していること
  - テストDB（pytest-django）が使用されること
  - `sizes` / `ranks` のマスタが登録済みであること
- 手順
  - `harvest_register.html` で日付/ロット/サイズ/ランク別の重量（kg）を入力し送信
  - APIは各入力セルに対して `POST /tablet/harvest/{date}?lot=...&size=...&rank=...` を送信（body: `{ "count": <g> }`）
- 期待結果
  - ステータスコードが 201（または上書きの場合 200）であること
  - `harvest_records` に `lot_name` / `size_id` / `rank_id` / `count(g)` が登録されていること
  - `GET /harvest/amount/daily` の集計値が登録内容に反映されること
