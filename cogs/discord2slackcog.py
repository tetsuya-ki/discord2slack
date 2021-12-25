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

        # Embed
        fields = []
        if len(message.embeds) != 0:
            for embed in message.embeds:
                dicted_data = embed.to_dict()
                LOG.info(dicted_data)
                description = f'>>> {embed.description}'
                field = {
                            'title' : 'Embed Text'
                            , 'value' : description
                        }
                FIELDS = 'fields'
                CREATED_AT = '作成日時'
                FROM_CHANNEL = '元のチャンネル'
                NAME = 'name'
                VALUE = 'value'
                fields.append(field)
                if FIELDS in dicted_data:
                    discord_fields = dicted_data[FIELDS]
                    LOG.info(discord_fields)
                    for discord_field in discord_fields:
                        if CREATED_AT == discord_field[NAME]:
                            field = {
                                'title' : CREATED_AT
                                , 'value' : discord_field[VALUE]
                                , 'short' : 'true'
                            }
                        elif FROM_CHANNEL == discord_field[NAME]:
                            channel_name = self._get_channel_name(discord_field[VALUE], message.guild)
                            field = {
                                'title' : FROM_CHANNEL
                                , 'value' : f'#{channel_name}'
                                , 'short' : 'true'
                            }
                        fields.append(field)

        # 本文
        main = {
            'mrkdwn_in': ['text'],
            'author_name': message.author.display_name,
            'author_icon': avatar_url,
            'text': message.clean_content,
            'fields': fields,
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

    def _get_channel_name(self, text:str, guild:discord.Guild):
        if text.count('#') == 1:
            channel_id = text.split('#')[1].split('>')[0]
            LOG.debug(f'check channel:{channel_id}')
            channel_info = None
            if channel_id.isdecimal():
                channel_info = guild.get_channel(int(channel_id))
            if channel_info is not None:
                return channel_info.name
        return '不明なチャンネル'

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    LOG.info('Discord2SlackCogを読み込む！')
    bot.add_cog(Discord2SlackCog(bot))  # Discord2SlackCogにBotを渡してインスタンス化し、Botにコグとして登録する。
