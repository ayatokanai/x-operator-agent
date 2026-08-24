# x-operator

AIを活用した自律型X（旧Twitter）運用エージェントプラットフォーム。
RSSフィードからのニュースキュレーション、AIによる価値評価・ドラフト生成、投稿実績に基づく自己学習（フィードバックループ）を自動化します。

---

## 🛠 アーキテクチャ・技術スタック

* **Language:** Python 3.12
  - lambda実行環境に合わせて`3.12`に設定
* **Cloud & Services:** AWS
  - **Lambda**: コード実行基盤
  - **DynamoDB**: 処理済み記事の重複管理、投稿履歴などのデータ保存
  - **EventBridge**: 定期的なジョブ実行のスケジューリング（Lambdaのトリガー）
* **Infrastructure as Code:** Terraform
* **LLM:** Google Gemini API (`gemini-2.5-flash`)
* **Environment:** Docker / Docker Compose

### DynamoDB テーブル設計（シングルテーブル設計）
テーブル名: x-operator-agent-table

主キー (Partition Key): id (String)

主な格納データ:
- システム設定: id = "SYSTEM:LAST_RUN" （前回の実行日時タイムスタンプ）
- 投稿履歴: id = "[記事URL]" （タイトル、投稿日時、ドラフト内容）

---

## 🚀 ローカル環境構築手順

1. リポジトリの準備と環境変数設定
   プロジェクトのルートに `.env` ファイルを作成し、必要な認証情報を設定します。

2. Dockerコンテナの起動
   Docker Composeを使用して、ローカル開発環境（Python 3.12 +Terraform + AWS CLI）をセットアップします。
   > [!TIP]
   > **おすすめの起動手順: VSCode Dev Containers**
   > 1. VSCodeでリポジトリを開く
   > 2. 左下の「><」から「Reopen in Container」を選択
   >    - VS Codeが `docker-compose.yml` を使ってコンテナを立ち上げ自動でコンテナ内部に入り込みます。
   > 3. 左下の表示が `Dev Container: x-operator-agent` になれば接続了

   - 手動でコンテナを建てる場合
      ```
      # コンテナのビルドとバックグラウンド起動
      docker compose up -d --build

      # コンテナ内部へログイン
      docker compose exec workspace bash
      ```

--- 

## ☁️ インフラのセットアップ (Terraform)
コンテナ内のターミナル（/workspace）で実行し、AWS上にDynamoDBテーブルを構築します。

```
# 1. 初期化
terraform init

# 2. 差分確認
terraform plan

# 3. リソース構築（プロンプトが出たら "yes" と入力）
terraform apply
```