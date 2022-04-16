# このBotについて

- Discordの指定されたチャンネルに投稿されたメッセージをSlackに連携し、Slackの指定されたチャンネルに投稿されたメッセージをDiscordに連携します
- 必要なもの
  - [環境変数#環境変数]を見てください
    - Discord側で必要なもの
    - Slack側必要なもの(ちょっと面倒)
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

- Slack投稿を有効にするDiscordのチャンネルID(複数ある場合は「;」を間に挟むこと)
- 例
  - 1件の場合: ALLOW_CHANNELS=18471289371923
  - 2件の場合: ALLOW_CHANNELS=18471289371923;1389103890128390

### SLACK_WEBHOOK_URL

- Slack投稿する際に使用するWEBHOOK_URLを1つだけ指定します(必須です)

### IGNORE_WEBHOOK_ID

- 無視するWebhook_id
  - 無視するWebhook_idを1つ指定できます。**指定しない場合、すべてのBotメッセージを無視します(Botの投稿はSlackに投稿しません)**
- 例: IGNORE_WEBHOOK_ID=18471289371923

### DISCORD_NAME

- Slackに投稿するフッターで表示する名前。**指定しない場合、Discordのギルド名が使用されます**
- 例: DISCORD_NAME=お茶会

### SLACK_BOT_TOKEN

- 必須です。あなたのSlackのBOTトークンを記載（トークンは厳重に管理し、公開されないよう配慮すること！）
  - `OAuth & Permissions`の`Bot User OAuth Token`から取得(同じ場所の`Bot Token Scopes`でScopeを設定すると取得できるようになる)
- 例: SLACK_BOT_TOKEN="xoxb-987654321123"

### SLACK_APP_TOKEN

- 必須です。あなたのSlackのAPPトークンを記載（トークンは厳重に管理し、公開されないよう配慮すること！）
  - `Basic Information`の`App-Level Tokens`から取得
  - `Generate Token and Scopes`ボタンを押して、`App-level tokens`を取得する必要あり(Scopeは`connections:write`)
- 例: SLACK_BOT_TOKEN="xapp-1-987654321123"

### SLACK_BOT_IDS

- SlackのWebhook URL(SLACK_WEBHOOK_URL)に入っているIDをコンマ区切りで入力(このBOT_IDは無視する(Discordに連携しない))
  - 本当は勝手に無視するようにしたかったが、Slackに登録されるBOT_IDとWEBHOOKで投稿されるときのBOT_IDが異なっているため自動で判別できなかった
  - Webhookを使わない仕組みならこんな無駄なことはしなくて良いのだろうけど、、、それはわからなかった。。。
- 例:
  - `https://hooks.slack.com/services/<team_id>/<BOT_ID>/<WEBHOOK_ID>`
    - SlackのWebhookを作るとこういう感じでURLが取得できるとする(上はテキトーです)
    - まんなかのやつ(BOT_ID)がココで設定したいBOT_IDです
    - 無視したいWEBHOOKが複数ある場合もあると思うのでこういう形式にしています

### DISCORD_WEBHOOK_URL

- Discord投稿する際に使用するWEBHOOK_URLを1つだけ指定します(必須です)

## 動かし方

### 前提

- poetryがインストールされていること
- Slack側でAppが作成されており、BOTトークン、APPトークン、Webhookが作成されていること
  - `OAuth & Permissions`の`Bot Token Scopes`で以下が有効であること
    1. `channels:history`
    2. `chat:write`
    3. `incoming-webhook`
    4. `users:read`
  - AppのSocket ModeがONになっていること
  - `Event Subscriptions`の`Enable Event`がONであること
    - 「Socket Mode is enabled. You won’t need to specify a Request URL.」と書いてあること
    - `Subscribe to bot events`で以下が有効であること
      1. `message.channels`
  - Slackで該当のチャンネルのインテグレーションにAppが追加されていること
    - チャンネルに追加されていないと、チャンネルの内容を読み込むことができないため
- `.env`が作成されていること

### 動かす

- 以下のコマンドを実行

```sh
poetry install
poetry run python discord2slackbot.py
```
