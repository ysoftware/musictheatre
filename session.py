import pickle
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from core import main_channel, bot_test, debug

configFile = "./session.pk"

# spreadsheet

def auth():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('./env/credentials.json', scope)
    gc = gspread.authorize(credentials)

    print(credentials)
    print(gc)

    spreadsheet_key = open('./env/sheet_id.txt', 'r').read().strip()
    print(spreadsheet_key)

    sheet = gc.open_by_key(spreadsheet_key)
    print(sheet)

    worksheet = sheet.get_worksheet(0)
    print(worksheet)

    return worksheet

# wrappers

def send(bot, message, parse_mode="Markdown"):
    bot.sendMessage(main_channel(), message, parse_mode)

def reply(update, message):
    update.message.reply_html(message)

# session persistence

def emptyConfig():
    print("emptying config...")
    obj = dict()
    obj['isPlaying'] = False
    return obj

def saveConfig(config):
    with open(configFile, "wb") as fi:
        pickle.dump(config, fi)
        print("saving {}".format(config))

def loadConfig():
    try:
        with open(configFile, "rb") as fi:
            config = pickle.load(fi)
            print("loaded {}".format(config))
            return config
    except Exception as e:
        print("could not read session.pk. creating a new one")
        print(e)
        config = emptyConfig()
        saveConfig(config)
        return config

# debug

def log(bot, message):
    if debug:
        bot.sendMessage(bot_test, "DEBUG: " + message)