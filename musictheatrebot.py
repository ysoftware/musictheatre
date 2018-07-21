from telegram.ext import Updater, CommandHandler
import sched, time, random, logging, pickle, datetime, calendar
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)
import datetime
import numbers
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# spreadsheet
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
wks = None
def auth():
    global wks
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open_by_key("1ExwdtbLUBpWZ12fg2faURtZLf7T8VZa0tndEX4SYkck").get_worksheet(0)

configFile = "./session.pk"
watb = -1001049406492
newseeds = -1001138132564
retardStickerId = "CAADBAAD2wADeyqRC60Pvd---1a5Ag";

admins = [
          "Xanes",
          "ysoftware",
          "tbshfmn",
          "sexy_nutella_69",
          "amobishoproden",
          "Doomgoat",
          "Tom_veldhuis"
          ]

# utilities

fValue = lambda cell: cell.value
fNonEmpty = lambda value: value
fLower = lambda value: value.lower()

# time

def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0

def checkAccess(update):
    return update.message.from_user.username in admins

def isNewCommand(update):
    timenow = unix_time_millis(datetime.datetime.now())
    messageTime = unix_time_millis(update.message.date)
    dt = timenow - messageTime
    print(update.message.text + " from " + update.message.from_user.username + " delayed by {}".format(dt))
    return dt < (20000)

def isNewSeeds(update):
    print(update.message.chat_id == newseeds)
    print(update.message.chat_id)
    return update.message.chat_id == newseeds

# quotes

def randomCunt():
    return random.choice(["Ready Lets Go", "Here we go...", "Come to Daddy", "Oh boy, here I go killin' again!"])

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
        print("config file is not found")
        config = emptyConfig()
        saveConfig(config)
        return config

# - commands

# session

def over(bot, update):
    if not checkAccess(update):
        return
    config = loadConfig()
    print(config)
    if config['isPlaying'] == True:
        if isNewCommand(update):
            bot.sendMessage(newseeds, "#musictheatre it's OVER.")
        endSession()
    else:
        update.message.reply_text("You betcha it is.")

def abort(bot, update):
    if not checkAccess(update):
        return
    config = loadConfig()
    if config['isPlaying'] == True:
        if isNewCommand(update):
            bot.sendMessage(newseeds, "#musictheatre it's ABORTED.")
        endSession()
    else:
        update.message.reply_text("I'll abort you, you fucking bitch.")

def newAlbum(bot, update):
    if not isNewCommand(update):
        return
    if not checkAccess(update):
        return
    config = loadConfig()
    message = update.message.text.split(" ", 1)[1].strip()

    if config['isPlaying'] == False:

        # new artist - album
        if " - " in message:
            artistName = message.split(" - ", 1)[0].strip()
            albumName = message.split(" - ", 1)[1].strip()
            newAlbumSet(bot, config, artistName, albumName)

        # new 34
        elif int(message) >= 4:
            auth()
            info = map(fValue, wks.range("B{0}:E{0}".format(message, message)))
            newAlbumSet(bot, config, info[1], info[3], info[2], info[0])
            
            # archive as well
            archiveDo(bot, message)
    else:
        bot.sendMessage(newseeds, "We're still in session.")

def newAlbumSet(bot, config, artistName, albumName, year, suggested):
    config['isPlaying'] = True
    config['artist'] = artistName.encode('utf-8')
    config['album'] = albumName.encode('utf-8')
    config['track'] = ""

    text = ""
    if year is not None and suggested is not None:
        config['year'] = year.encode('utf-8')
        config['suggested'] = suggested.encode('utf-8')

        text = "#musictheatre New Album: {0} - {1} ({2}) [Suggested by: {3}]".format(config['artist'], config['album'], config['year'], config['suggested'])
    else:
        text = "#musictheatre New Album: {0} - {1}".format(config['artist'], config['album'])

    bot.sendMessage(newseeds, text)
    saveConfig(config)

def nextSong(bot, update):
    if not isNewCommand(update):
        return
    if not checkAccess(update):
        return
    config = loadConfig()
    if config['isPlaying'] == True:
        trackName = update.message.text.split(" ", 1)[1].strip()
        if len(trackName) > 0 and len(config['artist']) > 0 and trackName != config['track']:
            config['track'] = trackName
            text = "#musictheatre {0} - {1}".format(config['artist'].encode('utf-8'), config['track'].encode('utf-8'))
            bot.sendMessage(newseeds, text)
            saveConfig(config)
    else:
        bot.sendMessage(newseeds, "What album was that again?")

def endSession():
    saveConfig(emptyConfig())

# current

def currentAlbum(bot, update):
    if not isNewCommand(update):
        return
    config = loadConfig()
    if config['isPlaying'] == True:
        if len(config['artist']) > 0 and len(config['album']) > 0:
            text = "{0} by {1}".format(config['album'].encode('utf-8'), config['artist'].encode('utf-8'))
            if config['year'] is not None:
                text += " ({})".format(config['year'].encode('utf-8'))
            if config['suggested'] is not None:
                text += " [Suggested by: {}]".format(config['suggested'].encode('utf-8'))
            update.message.reply_text(text)
    else:
        update.message.reply_text("Nothing is playing.")


def currentTrack(bot, update):
    if not isNewCommand(update):
        return
    config = loadConfig()
    if config['isPlaying'] == True:
        if len(config['artist']) > 0 and len(config['album']) > 0 and len(config['track']) > 0:
            text = "Now playing: {0} - {1} (from {2})".format(config['artist'].encode('utf-8'), config['track'].encode('utf-8'), config['album'].encode('utf-8'))
            update.message.reply_text(text)
    else:
        update.message.reply_text("Nothing is playing.")

# countdown

def cunt(bot, update):
    if not isNewCommand(update):
        return
    if checkAccess(update):
        message = [1]
        if len(update.message.text.split(" ", 1)) > 1:
            message = update.message.text.split(" ", 1)[1].strip()
            print(message)
        else:
            message = randomCunt()
        bot.sendMessage(newseeds, message.encode('utf-8'))
        count = 5
        while count:
            bot.sendMessage(newseeds, "{}".format(count))
            time.sleep(1)
            count -= 1
        bot.sendMessage(newseeds, "PLAY!")

# roll

def roll(bot, update):
    if not isNewCommand(update):
        return
    if not checkAccess(update):
        return
    config = loadConfig()
    print(config)

    if config['isPlaying'] == False:
        auth()
        suggestionNames = filter(fNonEmpty, map(fValue, wks.range('B4:B100')))
        illegalNames = map(fLower, filter(fNonEmpty, map(fValue, wks.range('G4:G1000')))[-5:])
        suggestionsCount = len(suggestionNames)
        print(illegalNames)
        if suggestionsCount > 0:
            for _ in range(5):
                result = random.randint(0, suggestionsCount-1)
                spreadsheetNumber = result + 4
                rolled = map(fValue, wks.range('A'+str(spreadsheetNumber)+':E'+ str(spreadsheetNumber)))
                if not rolled[1].lower() in illegalNames:
                    bot.sendMessage(newseeds,
                        "<b>Rolled {}</b>\n{} - {} ({})\nSuggested by: {}" .format(spreadsheetNumber, rolled[2].encode('utf-8'), rolled[4].encode('utf-8'), rolled[3].encode('utf-8'), rolled[1].encode('utf-8')), parse_mode="HTML")
                    return
                else:
                    bot.sendMessage(newseeds, "Rolled {}. {} - illegal.".format(spreadsheetNumber, rolled[1].encode('utf-8')))
        else:
            update.message.reply_text("No suggestions found.")
    else:
    	update.message.reply_text("Another session is still on. I'm afraid I can't do that.")

# archive

def archive(bot, update):
    if not isNewCommand(update):
        return
    if not checkAccess(update):
        return
    auth()
    position = int(update.message.text.split(" ")[1])
    archiveDo(bot, position)
    
def archiveDo(bot, position):
    now = datetime.datetime.now()

    suggestionNames = filter(fNonEmpty, map(fValue, wks.range('B4:B100')))
    lastSuggestion = len(suggestionNames) + 4

    archiveNames = filter(fNonEmpty, map(fValue, wks.range('G4:G1000')))
    archiveNewPosition = len(archiveNames) + 4

    # add to archive

    rolledCells = wks.range('B'+str(position)+':E'+ str(position))
    rolled = map(fValue, rolledCells)

    # add to archive
    archiveCells = wks.range('F'+str(archiveNewPosition)+':J'+str(archiveNewPosition))
    archiveCells[0].value = now.strftime("%d %b %y")
    archiveCells[1].value = rolled[0]
    archiveCells[2].value = rolled[1]
    archiveCells[3].value = rolled[2]
    archiveCells[4].value = rolled[3]

    wks.update_cells(archiveCells)

    # remove cells
    for cell in rolledCells:
        cell.value = ""

    # move cells up
    suggestionCells = wks.range('B'+str(position)+':E'+str(lastSuggestion))
    for i in range(len(suggestionCells)):
        if len(suggestionCells) > i + 4:
            suggestionCells[i].value = suggestionCells[i+4].value
        else:
            suggestionCells[i].value = ""

    wks.update_cells(rolledCells + suggestionCells)

    bot.sendMessage(newseeds, "Suggestion moved to the archive.")

# suggest

def suggest(bot, update):
    if not isNewCommand(update):
        return
    config = loadConfig()
    if config['isPlaying'] == False:
        bot.sendMessage(newseeds, "<b>Anyone in for a </b>#musictheatre<b> session?</b>", parse_mode="HTML")
    else:
        bot.sendMessage(newseeds, "The session is still on, isn't it? ISN'T IT?")

# help

def start(bot, update):
    update.message.reply_text("<b>Welcome to Music Theatre!</b>\nThis bot is designed to assist newseeds to discover music.\n", parse_mode="HTML")
    help(bot, update)

def help(bot, update):
    if not isNewCommand(update):
        return
    if not checkAccess(update):
        return
    update.message.reply_text("Here's the list of commands:\n<b>/sheet</b> gives you the link to our spreadsheet\n<b>/tagme</b> to subscribe to session notifications [private message only]\n<b>/suggest</b> will ask if anyone wants to start a session\n<b>/admins</b> for the list of people who have admin access\n\nUse these while in session:\n<b>/song</b> or <b>/album</b> to find out what's playing".encode('utf-8'), parse_mode="HTML")

def adminHelp(bot, update):
    if not isNewCommand(update):
        return
    update.message.reply_text("Here's the list of admin commands:\n<b>/roll</b> to randomly pick a suggestion\n<b>/cunt</b> to initiate the countdown\n<b>/archive [roll]</b> to archive a suggestion\n<b>/new [roll]</b> will set current album playing and archive the suggestion\n\nUse these while in session:\n<b>/n</b> to set current song playing\n<b>/over or /abort</b> to end the session".encode('utf-8'), parse_mode="HTML")

# say something

def say(bot, update):
    if not isNewCommand(update):
        return
    if not checkAccess(update):
        return
    if update.message.chat_id == newseeds:
        return
    message = update.message.text.split(" ", 1)[1].strip()
    bot.sendMessage(newseeds, message.encode('utf-8'), parse_mode="HTML")

def sticker(bot, update):
    if not isNewCommand(update):
        return
    if not checkAccess(update):
        return
    if isNewSeeds(update):
        return
    message = update.message.text.split(" ", 1)[1].strip()
    bot.sendSticker(newseeds, message)

# admins

def adminList(bot, update):
    if not isNewCommand(update):
        return
    text = "These <i>(%username%)</i>s have access to the bot's #musictheatre session commands:\n"
    for name in admins:
        text += "- " + name + "\n"
    text += "If they are not around, God help you."
    update.message.reply_text(text.encode('utf-8'), parse_mode="HTML")

# spreadshit link

def shit(bot, update):
    if not isNewCommand(update):
        bot.sendMessage(newseeds, "Hey folks, our spreadshit is here: http://bit.ly/mtheatre", parse_mode="HTML")
    else:
        update.message.reply_text("Here's the link to our spreadshit: http://bit.ly/mtheatre")

# tag

def tagPeople(bot, update):
    if not isNewCommand(update):
        return
    if not checkAccess(update):
        return
    if not isNewCommand(update):
        return
    config = loadConfig()
    if 'tagList' in config and len(config['tagList']) > 0:
        bot.sendMessage(newseeds, "Notifying {} people... (/taginfo for learn).".format(len(config['tagList'])))
        for id in config['tagList']:
            bot.sendMessage(id, "#musictheatre How about some music?")
    else:
        bot.sendMessage(newseeds, "No one is subscribed for /tag updates.")

def tagMe(bot, update):
    if isNewSeeds(update):
        update.message.reply_text("You have to private message me this command, because I am forbidden to initiate a chat with you.")
    else:
        id = update.effective_user.id
        config = loadConfig()
        if 'tagList' not in config:
            config['tagList'] = []
        if id not in config['tagList']:
            config['tagList'].append(id)
            bot.sendMessage(id, "You are now subscribed to /tag updates. Use /stop to unsubscribe.")
        else:
            bot.sendMessage(id, "You are already subscribed to /tag updates.")
        saveConfig(config)

def dontTagMe(bot, update):
    id = update.effective_user.id
    config = loadConfig()
    if 'tagList' not in config and id not in config['tagList']:
        config['tagList'] = []
        bot.sendMessage(id, "You are not subscribed to /tag updates.")
    else:
        config['tagList'].remove(id)
        bot.sendMessage(id, "You are now unsubscribed from /tag updates.")
    saveConfig(config)

def taginfo(bot, update):
    bot.sendMessage(newseeds, "PM /tagme to the bot to subscribe to #musictheatre updates.")

# retarded

def slow(bot, update):
	bot.sendSticker(newseeds, retardStickerId)

# work

def test(bot, update):
    if not isNewCommand(update):
        return
    if update.message.from_user.username == "ysoftware":
        bot.sendMessage(101193334, loadConfig())

def error_callback(bot, update, error):
    print(error)

# commands

logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
updater = Updater('337143431:AAH1TZLyqBTuHEKIIZ7OvEnmNL03I-EcHRM')

# sheet
updater.dispatcher.add_handler(CommandHandler('shit', shit))
updater.dispatcher.add_handler(CommandHandler('sheet', shit))
updater.dispatcher.add_handler(CommandHandler('spreadshit', shit))
updater.dispatcher.add_handler(CommandHandler('spreadsheet', shit))

# user session
updater.dispatcher.add_handler(CommandHandler('suggest', suggest))
updater.dispatcher.add_handler(CommandHandler('song', currentTrack))
updater.dispatcher.add_handler(CommandHandler('album', currentAlbum))
updater.dispatcher.add_handler(CommandHandler('tag', tagPeople))

# session notifications
updater.dispatcher.add_handler(CommandHandler('tagme', tagMe))
updater.dispatcher.add_handler(CommandHandler('stop', dontTagMe))
updater.dispatcher.add_handler(CommandHandler('fuckoff', dontTagMe))
updater.dispatcher.add_handler(CommandHandler('unsub', dontTagMe))
updater.dispatcher.add_handler(CommandHandler('taginfo', taginfo))

# admin 
updater.dispatcher.add_handler(CommandHandler('test', test))
updater.dispatcher.add_handler(CommandHandler('s', sticker))
updater.dispatcher.add_handler(CommandHandler('b', say))

# admin session 
updater.dispatcher.add_handler(CommandHandler('roll', roll))
updater.dispatcher.add_handler(CommandHandler('archive', archive))
updater.dispatcher.add_handler(CommandHandler('cunt', cunt))
updater.dispatcher.add_handler(CommandHandler('new', newAlbum))
updater.dispatcher.add_handler(CommandHandler('n', nextSong))
updater.dispatcher.add_handler(CommandHandler('abort', abort))
updater.dispatcher.add_handler(CommandHandler('over', over))

# other 
updater.dispatcher.add_handler(CommandHandler('slow', slow))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('adminHelp', adminHelp))
updater.dispatcher.add_handler(CommandHandler('admins', adminList))


updater.dispatcher.add_error_handler(error_callback)

updater.start_polling()
updater.idle()
