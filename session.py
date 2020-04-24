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
    return gc.open_by_key("1ExwdtbLUBpWZ12fg2faURtZLf7T8VZa0tndEX4SYkck").get_worksheet(0)

configFile = "./session.pk"

# wrappers

def send(bot, message, parse_mode="Markdown"):
    bot.sendMessage(newseeds, message, parse_mode)

def reply(update, message):
    update.message.reply_text(message)

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