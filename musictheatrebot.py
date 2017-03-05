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

def rfa():
    return random.choice(["SHITTY", "CRAPPY", "GOD DAMN", "FUCKING", "RETARDED", "STUPID", "FAGGY", "MOTHERFUCKING", "CANCEROUS"])

def rfn():
    return random.choice(["SHIT", "FUCK", "TRASH", "BITCH", "ASS", "ANALCONDA", "CRAP", "DIRT", "VAGINA", "DOGSHIT", "ASSCAKE", "FAIRY TITS", "CUMSTAIN", "HOMUNCULUS", "BABY ARM", "CUNT", "MEATFLAP"])

def randomWorstTime():
    return random.choice(["This is the <b>WORST TIME EVER!!!</b>",
                          "<b>REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE</b>",
                          "UHLFKUEGHDSNIUFBSR:AWNFPCOAWIFMVNALIKESBHUNFGUKVSHJBNVGH <b>: < </b>",
                          "{0} The Universe hasn't seen such <b>WORST TIME</b> in its whole <b>{1} HISTORY</b> of time! <b>EVER</b>".format(rfn(), rfa()),
                          "LITERALLY THE WORST TIMING POSSIBLE",
                          "NO NO NO NO STOP THAT NOT NOW",
                          "NOOO FOR {}'S SAKE, NOT NOW, WE'RE BUSY!!!!".format(rfn()),
                          "FUCK YOU WITH YOUR {0} LINKS YOU {1}".format(rfa(), rfn())
                         ])

def randomCunt():
    return random.choice(["Turn off your fucking shuffle, I'ma cunt!",
                          "OK! Shut the fuck up, I'm the boss in here!",
                          "Shut up and Dance! In...",
                          "Are you bitches ready? Starting the coundoooown!",
                          "Ready Lets Go",
                          "Everybody SHUT UP and listen!"])

def randomMango(name):
    return random.choice(["{} is gay for memes.".format(name),

                          "{} <b>HATES IT!</b>".format(name),
                          "This reminds {} of <b>Moderat</b>!".format(name),
                          "This is the <b>WORST {0}</b> that {1} has <b>EVER</b> heard!".format(rfn(), name),
                          "{0} thinks, <b>THIS SONG IS {1}!</b>".format(name, rfn()),
                          "{0} thinks, <b>THIS SONG IS {1} {2}!</b>".format(name, rfa(), rfn()),
                          "Did you even listen to it? God, {}...".format(name),
                          "<i>{} would rather have a buffalo take a </i><b>diarrhea dump</b><i> in his ear.</i>".format(name),
                          
                          "Pitchfork would rate this <b>{0}</b> out of <b>{1}!</b>".format(rfn(), rfn()),
                          "Bitchfork would rate this <b>SHIT</b> out of <b>SHIT!</b>",

                          "This sounds like that awesome song but all the good bits replaced with <b>{0} {1}</b>!".format(rfa(), rfn()),
                          "<i>{} MANGO RIP OFF</i>".format(rfa()),
                          "<b>{} MANGOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO</b>".format(rfa()),
                          "<b>MANGOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO</b>",
                          "<b>WHALE'S VAGINA!</b>",
                          "This crap should <b>BURN in HELL.</b>",
                          "What a stupid song! If only this shit artist knew his gear.",

                          "The only positive thing about this, is the artist's HIV-status.",
                          "This sounds like a <b>DOG</b> pissing straight up INTO MY {0}HOLES!".format(rfn()),
                          "It is with great disappointment, that I, {0}, musteth announce, that this is indeed <b>{1} {2} TRASH</b>." .format(name, rfa(), rfn()),
                          "This is now banned in China and soon this {0} will be banned <b>EVERYWHERE!</b>".format(rfn()),
                          "{0} thinks this is great music for on the road because it sounds like a fucking car crash WITH {1} EVERYWHERE.".format(name, rfn()),
                          "NORMIE MUSIC <b>REEEEEEEEEEEEEEEEEEEEEEEEEE!!</b>",
                          "If {0} were to smash his/her face against a piano WITH {1} ALL OVER HIS/HER FACE, it would still sound better than <b>THIS {2} {3}</b>.".format(name, rfn(), rfa(), rfn()),
                          "<i>{} is jealous of the fucking deaf</i>.".format(name)
                          ])

# help

def help(bot, update):
    update.message.reply_text("Here's the list of available commands:\n<b>/spreadshit</b> gives you the link to our spreadshit\n<b>/suggest</b> bot will ask if anyone wants to start a session\n<b>/admins</b> for the list of people who can control this bot\n\nUse these while in session:\n<b>/song</b> or <b>/album</b> to find out what's playing\n<b>/time</b> in case of like the worst time ever\n<b>/mango</b> to express your feelings about the current song".encode('utf-8'), parse_mode="HTML")

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
updater.dispatcher.add_handler(CommandHandler('mango', mango))
updater.dispatcher.add_handler(CommandHandler('time', badTiming))
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
