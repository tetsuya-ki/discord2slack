# このBotについて

- Discordの指定されたチャンネルに投稿されたメッセージをSlackに連携します
- 必要なもの
  - DISCORD_TOKEN: DiscordのBotを動かすためのトークン
  - ALLOW_CHANNELS: Slackに投稿するDiscordのチャンネルのID
  - SLACK_WEBHOOK_URL: SlackのWebhook URL
- 考えてないもの
  - 2022年4月のメッセージコンテントのやつ(小規模なBotとして実行されることを想定/多分動くはず)

## 環境変数

### DISCORD_TOKEN

- 必須です。あなたのDiscordのトークンを記載（トークンは厳重に管理し、公開されないよう配慮すること！）
- 例: DISCORD_TOKEN="fdj2iur928u42q4u239858290"

### LOG_LEVEL

- ログレベル(DEBUG/INFO/WARNING/ERROR)
- 例: LOG_LEVEL="INFO"

### ALLOW_CHANNELS

- Slack投稿を有効にするチャンネルID(複数ある場合は「;」を間に挟むこと)
- 例
  - 1件の場合: ALLOW_CHANNELS=18471289371923
  - 2件の場合: ALLOW_CHANNELS=18471289371923;1389103890128390

### SLACK_WEBHOOK_URL

- Slack投稿する際に仕様するWEBHOOK_URLを1つだけ指定します(必須です)

### IGNORE_WEBHOOK_ID

- 無視するWebhook_id
  - 無視するWebhook_idを1つ指定できます。**指定しない場合、すべてのBotメッセージを無視します(Slackに投稿しません)**
- 例: IGNORE_WEBHOOK_ID=18471289371923

## 動かし方

### 前提

- poetryがインストールされていること
- `.env`が作成されていること

### 動かす

- 以下のコマンドを実行

```sh
poetry install
poetry run python discord2slackbot.py
```
