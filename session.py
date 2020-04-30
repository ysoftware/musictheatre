import pickle
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from core import main_channel

configFile = "./session.pk"

# spreadsheet

def auth():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    gc = gspread.authorize(credentials)

    spreadsheet_key = open('sheet_id.txt', 'r').read()
    return gc.open_by_key(spreadsheet_key).get_worksheet(0)

# wrappers

def send(bot, message, parse_mode="Markdown"):
    log(bot, main_channel())
    log(bot, message)
    bot.sendMessage(main_channel(), message, parse_mode)

def reply(update, message):
    update.message.reply_html(message)

# session persistence

def emptyConfig():
    obj = dict()
    obj['isPlaying'] = False
    return obj

def saveConfig(config):
    with open(configFile, "wb") as fi:
        pickle.dump(config, fi)
        print("- {}".format(config))

def loadConfig():
    try:
        with open(configFile, "rb") as fi:
            config = pickle.load(fi)
            return config
    except:
        config = emptyConfig()
        saveConfig(config)
        return config

# debug

def log(bot, message):
    bot.sendMessage(bot_test, "DEBUG: " + message)