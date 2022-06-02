from core import isNewCommand, checkAccess, isNewSeeds, getTime, admins, main_channel, checkDevAccess, debug
from session import saveConfig, loadConfig, send, reply, auth, log
from utility import fValue, fNonEmpty, fLower
import numpy, subprocess, random

retardStickerId = "CAADBAAD2wADeyqRC60Pvd---1a5Ag";

# help

def start(update, context):
    reply(update, 
        "<b>Welcome to Music Theatre!</b>\nThis bot is designed to assist newseeds with discovering music.\n")
    help(update, update)

def help(update, context):
    if not isNewCommand(update): return
    if not checkAccess(update): return
    reply(update, "Here's the list of commands:\n<b>/sheet</b> gives you the link to our spreadsheet\n<b>/tagme</b> to subscribe to session notifications [private message only]\n<b>/suggest</b> will ask if anyone wants to start a session\n<b>/admins</b> for the list of people who have admin access\n\nUse these while in session:\n<b>/song</b> or <b>/album</b> to find out what's playing")

def adminHelp(update, context):
    if not isNewCommand(update): return
    reply(update, "Here's the list of admin commands:\n<b>/roll</b> to randomly pick a suggestion\n<b>/cunt</b> to initiate the countdown\n<b>/archive [roll]</b> to archive a suggestion\n<b>/new [roll]</b> will set current album playing and archive the suggestion\n\nUse these while in session:\n<b>/n</b> to set current song playing\n<b>/over or /abort</b> to end the session")

# say something

def say(update, context):
    if not isNewCommand(update): return
    if not checkAccess(update): return
    if isNewSeeds(update): return

    message = update.message.text.split(" ", 1)[1].strip()
    send(context.bot, message)

def sticker(update, context):
    if not isNewCommand(update): return
    if not checkAccess(update): return
    if isNewSeeds(update): return

    message = update.message.text.split(" ", 1)[1].strip()
    context.bot.sendSticker(main_channel(), message)

# admins

def adminList(update, context):
    if not isNewCommand(update): return

    text = "These <i>(%username%)</i>s have access to the bot's #musictheatre session commands:\n"
    for name in admins:
        text += "- " + name + "\n"
    text += "If they are not around, God help you."
    reply(update, text)

# spreadshit link

def shit(update, context):
    if not isNewCommand(update):
        send(context.bot, "Hey fags! Our spreadshit is here: http://bit.ly/mtheatre", parse_mode="HTML")
    else:
        reply(update, "Here's the link to our spreadshit: http://bit.ly/mtheatre")

# russian

def russian(update, context):
    if not isNewCommand(update): return
    send(context.bot, "Putin Hates Us All", parse_mode="HTML")

# toast

def toast(update, context):
    if not isNewCommand(update): return
    send(context.bot, "https://www.youtube.com/watch?v=beVRw_TnWsE", parse_mode="HTML")

# ball

def ball(update, context):
    if not isNewCommand(update): return

    message = random.choice(["It is certain", "It is decidedly so", "Without a doubt", "Yes - definitely", 
    "You may rely on it", "As I see it, yes", "Most likely", "Outlook good", "Signs point to yes", "Yes", 
    "All I see is fog", "Ask again later", "Better not tell you now", "Cannot predict now", 
    "Concentrate and ask again", "Don't count on it", "My reply is no", "My sources say no", 
    "Outlook not so good", "Very doubtful"])

    send(context.bot, message)

# tag

def tagPeople(update, context):
    if not isNewCommand(update): return
    if not checkAccess(update): return
    if not isNewCommand(update): return

    config = loadConfig()
    if 'tagList' in config and len(config['tagList']) > 0:
        send(context.bot, "Notifying {} people... (/taginfo to learn).".format(
            len(config['tagList'])))
        send(context.bot, "<b>Anyone in for a </b>#musictheatre<b> session?</b>", 
            parse_mode="HTML")
        for id in config['tagList']:
            if id != update.effective_user.id:
                try:
                    context.bot.sendMessage(id, "#musictheatre How about some music?")
                except:
                    print("{} blocked the bot.".format(id))
    else:
        send(context.bot, "No one is subscribed for /tag updates.")

def tagMe(update, context):
    if not isNewCommand(update): return

    if isNewSeeds(update):
        reply(update, 
            "You have to private message me this command, because I am forbidden to initiate a chat with you.")
    else:
        id = update.effective_user.id
        config = loadConfig()
        if 'tagList' not in config:
            config['tagList'] = []
        if id not in config['tagList']:
            config['tagList'].append(id)
            context.bot.sendMessage(id, "You are now subscribed to /tag updates. Use /stop to unsubscribe.")
        else:
            context.bot.sendMessage(id, "You are already subscribed to /tag updates.")
        saveConfig(config)

def dontTagMe(update, context):
    id = update.effective_user.id
    config = loadConfig()
    if 'tagList' not in config and id not in config['tagList']:
        config['tagList'] = []
        context.bot.sendMessage(id, "You are not subscribed to /tag updates.")
    else:
        config['tagList'].remove(id)
        context.bot.sendMessage(id, "You are now unsubscribed from /tag updates.")
    saveConfig(config)

def taginfo(update, context):
    reply(update, "Message the bot directly @MusicTheatreBot.\nStart the chat and say /tagme to get notified.")

def identify(update, context):
    id = update.effective_user.id
    reply(update, "Your telegram id is: {}".format(id))

# retarded

def slow(update, context):
    if not isNewCommand(update): return
    context.bot.sendSticker(main_channel(), retardStickerId)

# work

def test(update, context):
    if not isNewCommand(update): return
    if not checkDevAccess(update): return

    context.bot.sendMessage(update.message.from_user.id, loadConfig())

def removeRoll(update, context):
    if not isNewCommand(update):
        return
    if update.message.from_user.username == "ysoftware":
        config = loadConfig()
        config['lastRoll'] = None 
        saveConfig(config)

def error_callback(update, context):
    print("\n\n")
    print("Error occured!")
    print(context.error)
    print("\n\n")
