from cogs.modules import setting
from discord.ext import commands
from logging import basicConfig, getLogger
from datetime import timedelta, timezone
import discord, datetime
import keep_alive
import slack2discord

# 時間
JST = timezone(timedelta(hours=9), 'JST')
now = datetime.datetime.now(JST)

basicConfig(level=setting.LOG_LEVEL)
LOG = getLogger('discord2slackbot')

# 読み込むCogの名前を格納しておく。
INITIAL_EXTENSIONS = [
    'cogs.discord2slackcog'
]

class Discord2SlackBot(commands.Bot):
    # Discord2SlackBotのコンストラクタ。
    def __init__(self, command_prefix, intents):
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix, case_insensitive=True, intents=intents, help_command=None)
        LOG.info('cogを読むぞ！')

        # INITIAL_COGSに格納されている名前から、コグを読み込む。
        for cog in INITIAL_EXTENSIONS:
            self.load_extension(cog)

    async def on_ready(self):
        LOG.info('We have logged in as {0.user}'.format(self))
        LOG.info(f"### guilds length ### \n{len(self.guilds)}")
        LOG.debug(f"### guilds ### \n{self.guilds}")

# Discord2SlackBotのインスタンス化、および、起動処理
if __name__ == '__main__':
    intents = discord.Intents.all()
    intents.typing = False
    intents.members = False
    intents.presences = False

    bot = Discord2SlackBot(command_prefix='/', intents=intents)

    # start a server
    keep_alive.keep_alive()
    slack2discord.start_slack2discord()
    bot.run(setting.DISCORD_TOKEN)