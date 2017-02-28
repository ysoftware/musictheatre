from telegram.ext import Updater, CommandHandler
import sched, time, random, logging, pickle

# watb chat id "-1001049406492"

watb = "-1001049406492"

# access

def checkAccess(update):
    return update.message.from_user.username == "ysoftware" or update.message.from_user.username == "frederik81" or update.message.from_user.username == "tbshfmn" or update.message.from_user.username == "sexy_nutella_69" or update.message.from_user.username == "amobishoproden"

# edit
#
#def editartist(bot, update):
#
#def editalbum(bot, update):

# /join, /ready, /stav



# session

# suggested by ??

def over(bot, update):
    if not checkAccess(update):
        return
    config = load()
    if config[0] == True:
        bot.sendMessage(watb, "#musictheatre it's OVER.")
        endSession()

def abort(bot, update):
    if not checkAccess(update):
        return
    config = load()
    if config[0] == True:
        bot.sendMessage(watb, "#musictheatre it's ABORTED.")
        endSession()

def newAlbum(bot, update):
    if not checkAccess(update):
        return
    config = load()
    if config[0] == False:
        message = update.message.text.split(" ", 1)[1].encode('utf-8').strip()
        artistName = message.split(" - ", 1)[0].strip()
        albumName = message.split(" - ", 1)[1].strip()

        if len(albumName) > 2 and len(artistName) > 2:
            config[0] = True
            config[1] = artistName
            config[2] = albumName
            config[3] = ""
            text = "#musictheatre New Album: {0} - {1}".format(config[1], config[2]).encode('utf-8')
            bot.sendMessage(watb, text)
            save(config)

def nextSong(bot, update):
    if not checkAccess(update):
        return
    config = load()
    if config[0] == True:
        trackName = update.message.text.split(" ", 1)[1].strip().encode('utf-8')
        if len(trackName) > 2 and len(config[1]) > 2:
            config[3] = trackName
            text = "#musictheatre {0} - {1}".format(config[1], config[3]).encode('utf-8')
            bot.sendMessage(watb, text)
            save(config)

def endSession():
    save([False, "", "", ""])

# current

def currentTrack(bot, update):
    config = load()
    if config[0] == True:
        if len(config[1]) > 2 and len(config[2]) > 2 and len(config[3]) > 2:
            text = "Now playing: {0} - {1} (from {2})".format(config[1], config[3], config[2]).encode('utf-8')
            update.message.reply_text(text)

# persistence

def save(config):
    file = "session.pk"
    with open(file, "wb") as fi:
        pickle.dump(config, fi)
        print("- {}".format(config))

def load():
    try:
        file = "session.pk"
        with open(file, "rb") as fi:
            config = pickle.load(fi)
            return config
    except:
        print("config not found")
        save()
        return [False, "", "", ""]

# countdown

def cunt(bot, update):
    if checkAccess(update):
        bot.sendMessage(watb, "Turn off your fucking shuffle, I'ma cunt!")
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
    config = load()
    if config[0] == False:
        limit = int(update.message.text.split(" ")[1])
        if limit and limit >= 4:
            result = random.randint(4, limit)
            bot.sendMessage(update.message.chat_id, "Rolled <b>{}</b>.".format(result), parse_mode="HTML")

# suggest

def suggest(bot, update):
    if not checkAccess(update):
        return
    config = load()
    if config[0] == False:
        bot.sendMessage(watb, "<b>Anyone in for a </b>#musictheatre<b> session?</b>", parse_mode="HTML")

# bad timing

def badTiming(bot, update):
    config = load()
    if config[0] == True and config[3] != "":
        text = "This is the <b>WORST TIME EVER!!!</b>".encode('utf-8')
        bot.sendMessage(watb, text, parse_mode="HTML")

# mango

def mango(bot, update):
    config = load()
    if config[0] == True:
        name = "{0} {1}".format(update.message.from_user.first_name, update.message.from_user.last_name).strip()
        text = "{} <b>HATES IT!</b>".format(name).encode('utf-8')
        bot.sendMessage(watb, text, parse_mode="HTML")

# say something

def say(bot, update):
    if not checkAccess(update):
        return
    if update.message.chat_id == watb:
        return
    message = update.message.text.split(" ", 1)[1].strip().encode('utf-8')
    bot.sendMessage(watb, message)

# work

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

updater = Updater('337143431:AAHK2PvoU6-HV5EJb6ydlCGzlvnqj8YFFVs')

# general commands

updater.dispatcher.add_handler(CommandHandler('roll', roll))
updater.dispatcher.add_handler(CommandHandler('mango', mango))
updater.dispatcher.add_handler(CommandHandler('song', currentTrack))
updater.dispatcher.add_handler(CommandHandler('time', badTiming))

# session control

#updater.dispatcher.add_handler(CommandHandler('edit_artist', editartist))
#updater.dispatcher.add_handler(CommandHandler('edit_album', editalbum))

updater.dispatcher.add_handler(CommandHandler('suggest', suggest))
updater.dispatcher.add_handler(CommandHandler('cunt', cunt))
updater.dispatcher.add_handler(CommandHandler('new', newAlbum))
updater.dispatcher.add_handler(CommandHandler('n', nextSong))
updater.dispatcher.add_handler(CommandHandler('abort', abort))
updater.dispatcher.add_handler(CommandHandler('over', over))
updater.dispatcher.add_handler(CommandHandler('b', say))

updater.start_polling()
updater.idle()
