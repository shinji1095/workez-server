# workez-server

ETM2025で作成する椎茸自動仕分けシステムのプロトタイプ開発管理のためのリポジトリ．

---

- [workez-server](#workez-server)
- [システム構成](#システム構成)
- [Commit Message Guidelines](#commit-message-guidelines)
- [ブランチ管理](#ブランチ管理)
- [使い方](#使い方)
  - [1. 開発環境](#1-開発環境)
  - [1.1 環境変数の設定](#11-環境変数の設定)
  - [1.2 コンテナの作成](#12-コンテナの作成)
  - [1.3 実行確認](#13-実行確認)
  - [2. 本番環境](#2-本番環境)


# システム構成

システム構成を示す．

| 項目             | 技術 / ソフトウェア | バージョン |
|------------------|---------------------|------------|
| OS               | Ubuntu              | 24.04 LTS  |
| コンテナ         | Docker              | TBD       |
| VPN              | TBD                 | TBD         |
| フロントエンド   | React.js            | TBD       |
| バックエンド     | Django              | TBD       |
| データベース     | SQLite3             | TBD          |
| リバースプロキシ | nginx               | TBD       |
| IoT通信プロトコル          | mqtt-broker         | TBD       |
| IoTデバイス      | Raspberry Pi        | 5          |
| Raspberry Pi OS  | Ubuntu              | 24.04 LTS  |


# Commit Message Guidelines

コミットガイドラインに従いコミットすること．

| **Type**     | **Description**                                                                 |
|--------------|---------------------------------------------------------------------------------|
| feat         | 新機能の追加                                                                   |
| fix          | バグの修正                                                                      |
| docs         | ドキュメントのみの変更                                                      |
| style        | スペースやインデントなどコードの見た目の変更 |
| refactor     | リファクタリング                      |
| perf         | 機能のパフォーマンス向上（遅延時間を短縮など）                                     |
| test         | テストの追加，変更                                     |


# ブランチ管理

ブランチによって開発工程を管理し，バージョン管理を行う．

![](./docs/img/ブランチ管理.jpg)

# 使い方

## 1. 開発環境

## 1.1 環境変数の設定

コマンドを実行し`.env.local`と`.env.production`を作成する．

```shell
chmod +x ./generate_env.sh
./generate_env.sh          # 環境変数を作成

./generate_env.sh --force  # 上書き作成する場合
```

## 1.2 コンテナの作成

dockerコンテナを起動する．

```shell
docker compose up -d -f docker-compose.yml -f docker-compose.local.yml --build 
```

## 1.3 実行確認
TBD

## 2. 本番環境


TBD


