import pickle
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from core import newseeds

# spreadsheet

def auth():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    gc = gspread.authorize(credentials)

    spreadsheet_key = open('sheet_id.txt', 'r').read()
    return gc.open_by_key(spreadsheet_key).get_worksheet(0)

configFile = "./session.pk"

# wrappers

def send(bot, message, parse_mode="Markdown"):
    bot.sendMessage(newseeds, message, parse_mode)

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
    except Exception as e:
        print("could not read session.pk. creating a new one")
        print(e)
        config = emptyConfig()
        saveConfig(config)
        return config