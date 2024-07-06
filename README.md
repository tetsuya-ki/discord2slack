# このBotについて

- Discordの指定されたチャンネルに投稿されたメッセージをSlackに連携し、Slackの指定されたチャンネルに投稿されたメッセージをDiscordに連携します
- 手順の例
  - <https://scrapbox.io/marukot-ch/discord2slack%E3%81%AAbot%E3%82%92%E5%8B%95%E3%81%8B%E3%81%97%E3%81%A6%E3%81%BF%E3%82%88%E3%81%86>
- 必要なもの
  - [環境変数](#環境変数)と[前提](#前提)を見てください
    - Slack側必要なもの(ちょっと面倒)
    - Discord側で必要なもの
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
  - Webhookを使わない仕組みなら、こんなムダなことはしなくて良いのだろうけど、それはわからなかった……。
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
  - `poetry -V`して`Poetry version 1.x.x`が返ればOK
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
- [Discord側でBotが作成](https://discord.com/developers/applications/)されており、以下の状況であること
  - 作成したDiscord Botのトークンを取得していること
  - 特権インテントの一種であるメッセージ読み込み権限がONであること
    - Privileged Gateway IntentsのMESSAGE CONTENT INTENTがON(初期設定はOFF)
    - ＊[dicord.pyのゲートウェイインテント入門](https://discordpy.readthedocs.io/ja/latest/intents.html#privileged-intents)が分かりやすい
  - Slackに連携したいDiscord側チャンネルで、Webhook URLを作成していること
    - DiscordでWebhook URLを作成する方法は[こちら](https://support.discord.com/hc/ja/articles/228383668-%E3%82%BF%E3%82%A4%E3%83%88%E3%83%AB-Webhooks%E3%81%B8%E3%81%AE%E5%BA%8F%E7%AB%A0)
- cogs/module/filesに `.env`が作成され、各種環境変数が設定されていること
  - 同階層にある、`.env.sample`をコピーして作ると良い
  - 「作成され、各種環境変数が設定」と書いたが、環境変数として登録されている状態ならOK
    - たとえば、replitならToolsにあるsecretsで登録しておく
    - ![Alt text](image.png)

### 動かす

- 以下のコマンドを実行

```sh
poetry install
poetry run python discord2slackbot.py
```

## 今後直すメモ

- 後で見返したら、IGNORE_WEBHOOK_IDって何のために存在するの？　と思ったけど、DISCORD_WEBHOOK_URLで設定したURLの一部を使ってた
  - DISCORD_WEBHOOK_URLは必須だし、IGNORE_WEBHOOK_IDという名前が意味不明。これは自動的に設定するべき
  - BotはSlackに投げたくないって場合もありえるので、それは設定でON/OFFできてもいい気がする
- 動かなくなる可能性があるし、discord.pyのバージョンアップをしておきたい

## 変えたメモ

- 2024/4/19
  - discord2slackbot.py
    - keep_aliveをコメントアウト(もういらない気がする)
  - slack2discord.py
    - user_dictで投稿したユーザーを持つようにした(何回もSlackのAPI叩いたらユーザーリミット到達したため)
    - 文字が書かれてない場合は対象外とか、SLACK_BOT_IDSが未記載の場合Botは対象外とかした
