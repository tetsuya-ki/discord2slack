from discord.ext import commands
from logging import getLogger, log
from .modules import setting

import discord, aiohttp, json

LOG = getLogger('discord2slackbot')

# コグとして用いるクラスを定義。
class Discord2SlackCog(commands.Cog):
    # Discord2SlackCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # 読み込まれた時の処理
    @commands.Cog.listener()
    async def on_ready(self):
        LOG.debug(self.bot.guilds)

    # メッセージ送信時に実行されるイベントハンドラを定義
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # 自分は無視する
        if message.author == self.bot.user:
            return
        # IGNORE_WEBHOOK_IDが指定されていない場合、Botは無視。設定されている場合、そのWebhook_idの場合のみ無視
        if setting.IGNORE_WEBHOOK_ID is None:
            if message.author.bot:
                return
        elif message.webhook_id and message.webhook_id == int(setting.IGNORE_WEBHOOK_ID):
            return

        # 許可されているチャンネルのみ対応
        if message.channel.id in setting.ALLOW_CHANNELS:
            await self.post_to_slack(message)
        else:
            return

    async def post_to_slack(self, message: discord.Message):
        avatar_url = str(message.author.avatar_url).replace('.webp', '.png')
        guild_icon_url = str(message.guild.icon_url).replace('.webp', '.png')
        name = setting.DISCORD_NAME if setting.DISCORD_NAME else message.guild.name

        # 本文
        main = {
            'mrkdwn_in': ['text'],
            'author_name': message.author.display_name,
            'author_icon': avatar_url,
            'text': message.clean_content,
            'footer_icon': guild_icon_url,
            'footer': f'{name}@Discord Channel from: {message.channel.name}'
        }

        # 画像部
        images = []
        if len(message.attachments) != 0:
            for i, attachment in enumerate(message.attachments):
                if attachment.filename.endswith(('.jpg','.jpeg','.png','.gif',)):
                    image = {
                        'mrkdwn_in': ['text'],
                        'text': f'image - {i + 1}',
                        'image_url': attachment.url,
                    }
                    images.append(image)

        LOG.debug(main)
        datas = []
        datas.append(main)
        datas.extend(images)
        data =  json.dumps({'attachments': datas})
        LOG.debug(data)

        # 設定ないなら何もしない
        if setting.SLACK_WEBHOOK_URL is None:
            LOG.error('環境変数SLACK_WEBHOOK_URLにデータがありません！')
            return
        async with aiohttp.ClientSession() as session:
            headers = {'content-type': 'application/json'}
            async with session.post(setting.SLACK_WEBHOOK_URL, data=data, headers=headers) as resp:
                resp_text = await resp.text()
                LOG.info(f'Post to Slack! status:{resp.status} / text:{resp_text}')

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    LOG.info('Discord2SlackCogを読み込む！')
    bot.add_cog(Discord2SlackCog(bot))  # Discord2SlackCogにBotを渡してインスタンス化し、Botにコグとして登録する。
