from telegram.ext import Updater, CommandHandler
import sched, time, random, logging, pickle

watb = "-1001049406492"
admins = ["ysoftware", "frederik81", "tbshfmn",  "sexy_nutella_69", "amobishoproden"]

# access

def checkAccess(update):
    return update.message.from_user.username in admins

# session

def over(bot, update):
    if not checkAccess(update):
        return
    config = loadConfig()
    if config[0] == True:
        bot.sendMessage(watb, "#musictheatre it's OVER.")
        endSession()

def abort(bot, update):
    if not checkAccess(update):
        return
    config = loadConfig()
    if config[0] == True:
        bot.sendMessage(watb, "#musictheatre it's ABORTED.")
        endSession()

def newAlbum(bot, update):
    if not checkAccess(update):
        return
    config = loadConfig()
    if config[0] == False:
        message = update.message.text.split(" ", 1)[1].encode('utf-8').strip()
        artistName = message.split(" - ", 1)[0].strip()
        albumName = message.split(" - ", 1)[1].strip()

        if len(albumName) > 2 and len(artistName) > 2:
            config[0] = True
            config[1] = artistName
            config[2] = albumName
            config[3] = ""
            text = "#musictheatre New Album: {0} - {1}".format(config[1], config[2])
            bot.sendMessage(watb, text.encode('utf-8'))
            saveConfig(config)

def nextSong(bot, update):
    if not checkAccess(update):
        return
    config = loadConfig()
    if config[0] == True:
        trackName = update.message.text.split(" ", 1)[1].encode('utf-8').strip()
        if len(trackName) > 2 and len(config[1]) > 2 and trackName != config[3]:
            config[3] = trackName
            text = "#musictheatre {0} - {1}".format(config[1], config[3])
            bot.sendMessage(watb, text.encode('utf-8'))
            saveConfig(config)

def endSession():
    saveConfig([False, "", "", ""])

# edit

#def editArtist(bot, update):
#    if not checkAccess(update):
#        return
#    config = loadConfig()
#        if config[1] == True:
#
#
#def editSong(bot, update):
#    if not checkAccess(update):
#        return
#    config = loadConfig()
#        if config[3] == True:
#
#
#def editAlbum(bot, update):
#    if not checkAccess(update):
#        return
#    config = loadConfig()
#        if config[2] == True:


# current

def currentAlbum(bot, update):
    config = loadConfig()
    if config[0] == True:
        if len(config[1]) > 2 and len(config[2]) > 2:
            text = "{0} by {1}".format(config[2], config[1])
            update.message.reply_text(text.encode('utf-8'))

def currentTrack(bot, update):
    config = loadConfig()
    if config[0] == True:
        if len(config[1]) > 2 and len(config[2]) > 2 and len(config[3]) > 2:
            text = "Now playing: {0} - {1} (from {2})".format(config[1], config[3], config[2])
            update.message.reply_text(text.encode('utf-8'))

# session persistence

def saveConfig(config):
    file = "session.pk"
    with open(file, "wb") as fi:
        pickle.dump(config, fi)
        print("- {}".format(config))

def loadConfig():
    try:
        file = "session.pk"
        with open(file, "rb") as fi:
            config = pickle.load(fi)
            return config
    except:
        print("config file is not found")
        saveConfig()
        return [False, "", "", ""]

# countdown

def cunt(bot, update):
    if checkAccess(update):
        bot.sendMessage(watb, randomCunt().encode('utf-8'))
        count = 5
        while count:
            bot.sendMessage(watb, "{}".format(count))
            time.sleep(1)
            count -= 1
        bot.sendMessage(watb, "PLAY!")

# roll

def roll(bot, update):
    if not checkAccess(update):
        return
    config = loadConfig()
    if config[0] == False:
        limit = int(update.message.text.split(" ")[1])
        if limit and limit >= 4:
            result = random.randint(4, limit)
            bot.sendMessage(update.message.chat_id, "Rolled <b>{}</b>.".format(result), parse_mode="HTML")

# suggest

def suggest(bot, update):
    config = loadConfig()
    if config[0] == False:
        bot.sendMessage(watb, "<b>Anyone in for a </b>#musictheatre<b> session?</b>", parse_mode="HTML")

# bad timing

def badTiming(bot, update):
    config = loadConfig()
    if config[0] == True and config[3] != "":
        text = randomWorstTime()
        bot.sendMessage(watb, text.encode('utf-8'), parse_mode="HTML")

# mango

def mango(bot, update):
    config = loadConfig()
    if config[0] == True:
        name = "{0} {1}".format(update.message.from_user.first_name, update.message.from_user.last_name).strip()
        text = randomMango(name)
        bot.sendMessage(watb, text.encode('utf-8'), parse_mode="HTML")

# quotes

def randomCunt():
    return random.choice(["Turn off your fucking shuffle, I'ma cunt!",
                          "OK! Shut the fuck up, I'm the boss in here!",
                          "Shut up and Dance! In...",
                          "Are you bitches ready? Starting the coundoooown!",
                          "Ready Lets Go",
                          "Everybody SHUT UP and listen!"])


# help

def help(bot, update):
    update.message.reply_text("Here's the list of available commands:\n<b>/spreadshit</b> gives you the link to our spreadshit\n<b>/suggest</b> bot will ask if anyone wants to start a session\n<b>/admins</b> for the list of people who can control this bot\n\nUse these while in session:\n<b>/song</b> or <b>/album</b> to find out what's playing".encode('utf-8'), parse_mode="HTML")

# say something

def say(bot, update):
    if not checkAccess(update):
        return
    if update.message.chat_id == watb:
        return
    message = update.message.text.split(" ", 1)[1].strip()
    bot.sendMessage(watb, message.encode('utf-8'), parse_mode="HTML")

# admins

def adminList(bot, update):
    text = "These <i>(%username%)</i>s have access to the bot's #musictheatre session commands:\n"
    for name in admins:
        text += "- " + name + "\n"
    text += "If they are not around, God help you."
    update.message.reply_text(text.encode('utf-8'), parse_mode="HTML")

# spreadshit link

def shit(bot, update):
    update.message.reply_text("Here's the link to our spreadshit: http://bit.ly/watb-spreadshit")

# work

logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
updater = Updater('337143431:AAHK2PvoU6-HV5EJb6ydlCGzlvnqj8YFFVs')

# general commands

updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('admins', adminList))

updater.dispatcher.add_handler(CommandHandler('shit', shit))
updater.dispatcher.add_handler(CommandHandler('sheet', shit))
updater.dispatcher.add_handler(CommandHandler('spreadshit', shit))
updater.dispatcher.add_handler(CommandHandler('spreadsheet', shit))

updater.dispatcher.add_handler(CommandHandler('suggest', suggest))
updater.dispatcher.add_handler(CommandHandler('song', currentTrack))
updater.dispatcher.add_handler(CommandHandler('album', currentAlbum))

# admin commands

updater.dispatcher.add_handler(CommandHandler('roll', roll))
updater.dispatcher.add_handler(CommandHandler('cunt', cunt))
updater.dispatcher.add_handler(CommandHandler('new', newAlbum))
updater.dispatcher.add_handler(CommandHandler('n', nextSong))
updater.dispatcher.add_handler(CommandHandler('abort', abort))
updater.dispatcher.add_handler(CommandHandler('over', over))

updater.dispatcher.add_handler(CommandHandler('b', say))

updater.start_polling()
updater.idle()
