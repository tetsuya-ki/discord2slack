import os
from os.path import join, dirname
from dotenv import load_dotenv
from logging import DEBUG, INFO, WARNING, ERROR

def if_env(str):
    '''
    strをTrue／Falseに変換(NoneのときはFalse)
    '''
    if str is None:
        return False
    elif str.upper() == 'TRUE':
        return True
    else:
        return False

def get_log_level(str):
    '''
    ログレベルを設定(Noneや無効のときはWARNING)
    '''
    if str is None:
        return WARNING

    upper_str = str.upper()
    if upper_str == 'DEBUG':
        return DEBUG
    elif upper_str == 'INFO':
        return INFO
    elif upper_str == 'ERROR':
        return ERROR
    else:
        return WARNING

def get_split_data(str):
    '''
    「；」で分割したリストを取得
    '''
    return [] if str is None else list(map(int, str.split(';')))

# 環境変数をファイルから読み込む
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), 'files' + os.sep + '.env')
load_dotenv(dotenv_path)

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
LOG_LEVEL = get_log_level(os.environ.get('LOG_LEVEL'))
IS_HEROKU = if_env(os.environ.get('IS_HEROKU'))
IS_REPLIT = if_env(os.environ.get('IS_REPLIT'))
ALLOW_CHANNELS = get_split_data(os.environ.get('ALLOW_CHANNELS'))
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')
IGNORE_WEBHOOK_ID = os.environ.get('IGNORE_WEBHOOK_ID')
DISCORD_NAME = os.environ.get('DISCORD_NAME')