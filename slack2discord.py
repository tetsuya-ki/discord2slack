import time, json, requests, re
from threading import Thread
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from cogs.modules import setting
from logging import getLogger

LOG = getLogger('discord2slackbot')

# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(token=setting.SLACK_BOT_TOKEN)
test = ''

@app.event('message')
def handle_message_events(body):
    LOG.info(body)
    # LOG.debug(body['event'])
    if body['event'].get('bot_id') in setting.SLACK_BOT_IDS:
        return
    user = body['event'].get('user')
    if not user:
        user = body['event']['message']['user']

    name,icon = get_name_by_userid(body['event']['user'])
    LOG.debug(name)
    post = Thread(target=post_to_discord, args=(body, name,icon,))
    post.start()

def get_name_by_userid(userid):
    userslist = app.client.users_list()
    app.client.users_identity
    name = 'undifined'
    icon = None
    members = userslist['members']
    for member in members:
        if member['id'] == userid: 
            if member['real_name']:
                name = member['real_name']
            if member['profile'].get('display_name'):
                name = member['profile'].get('display_name')
            if member['profile'].get('image_512'):
                icon = member['profile'].get('image_512')
            break
    return name,icon

def post_to_discord(body, name, icon):
    footer_name = setting.DISCORD_NAME

    # 本文(Slack MD to Discord MD)
    message = body['event'].get('text')
    message = re.sub(r'\*(.+?)\*', r'**\1**', message) # 太字
    message = re.sub(r'_(.+?)_', r'*\1*', message) # 斜字
    message = re.sub(r'~(.+?)~', r'~~\1~~', message) # 取消
    message = re.sub(r'&gt;', '>', message)
    message = re.sub(r'&lt;', '<', message) 

    # 添付ファイル
    attachments = body['event'].get('attachments')
    if attachments:
        attachments = attachments[0] if len(attachments) > 0 else None
    exist_file = ''
    if body['event'].get('files') or (attachments and attachments.get('files')):
        exist_file = '(添付ファイルがSlackに有ったよ)'

    main = {
        'username': name,
        'content': exist_file,
        'embeds': [{
            'footer': {
                'text': f'{footer_name}@Slack'
            },
            'description': message
        }]
    }
    if icon:
        main['avatar_url']= icon

    # LOG.debug(main)
    data = json.dumps(main)
    LOG.debug(data)

    # 設定ないなら何もしない
    if setting.DISCORD_WEBHOOK_URL is None:
        LOG.error('環境変数Discord_WEBHOOK_URLにデータがありません！')
        return
    headers = {'content-type': 'application/json'}
    resp = requests.post(setting.DISCORD_WEBHOOK_URL, data=data, headers=headers)
    resp_text = resp.text
    LOG.info(f'Post to Discord! status:{resp.status_code} / text:{resp_text}')

# アプリを起動します
def run():
    SocketModeHandler(app, setting.SLACK_APP_TOKEN).start()

def wait(sleep_time):
    time.sleep(sleep_time)
    info = app.client.auth_test()
    global test
    test = info.get('user_id')
    LOG.debug(f'test: {test}')

def start_slack2discord():
    server = Thread(target=run)
    init = Thread(target=wait, args=(2,))
    server.start()
    init.start()
    LOG.debug('start!')