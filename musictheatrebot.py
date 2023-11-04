#!/usr/bin/python
from telegram.ext import Updater, CommandHandler
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)
import os
import logging

print("working dir", os.getcwd())

# add files
import core, session, today
import other_commands, start_commands, session_commands, sheet_commands

# setup bot

logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

telegram_token = open('./env/telegram_token.txt', 'r').read().strip()
updater = Updater(token=telegram_token)

# sheet
updater.dispatcher.add_handler(CommandHandler('shit', other_commands.shit))
updater.dispatcher.add_handler(CommandHandler('sheet', other_commands.shit))
updater.dispatcher.add_handler(CommandHandler('spreadshit', other_commands.shit))
updater.dispatcher.add_handler(CommandHandler('spreadsheet', other_commands.shit))

# user session
updater.dispatcher.add_handler(CommandHandler('suggest', start_commands.suggest))
updater.dispatcher.add_handler(CommandHandler('song', session_commands.currentTrack))
updater.dispatcher.add_handler(CommandHandler('album', session_commands.currentAlbum))
updater.dispatcher.add_handler(CommandHandler('tag', other_commands.tagPeople))

# session notifications
updater.dispatcher.add_handler(CommandHandler('tagme', other_commands.tagMe))
updater.dispatcher.add_handler(CommandHandler('stop', other_commands.dontTagMe))
updater.dispatcher.add_handler(CommandHandler('fuckoff', other_commands.dontTagMe))
updater.dispatcher.add_handler(CommandHandler('unsub', other_commands.dontTagMe))
updater.dispatcher.add_handler(CommandHandler('taginfo', other_commands.taginfo))

# developer commands
updater.dispatcher.add_handler(CommandHandler('test', other_commands.test))

# admin 
updater.dispatcher.add_handler(CommandHandler('s', other_commands.sticker))
updater.dispatcher.add_handler(CommandHandler('b', other_commands.say))
updater.dispatcher.add_handler(CommandHandler('removeRoll', other_commands.removeRoll))

# admin session 
updater.dispatcher.add_handler(CommandHandler('roll', start_commands.roll))
updater.dispatcher.add_handler(CommandHandler('cunt', start_commands.cunt))
updater.dispatcher.add_handler(CommandHandler('archive', sheet_commands.archive))
updater.dispatcher.add_handler(CommandHandler('new', session_commands.newAlbum))
updater.dispatcher.add_handler(CommandHandler('n', session_commands.nextSong))
updater.dispatcher.add_handler(CommandHandler('abort', session_commands.abort))
updater.dispatcher.add_handler(CommandHandler('over', session_commands.over))

# other 
updater.dispatcher.add_handler(CommandHandler('slow', other_commands.slow))
updater.dispatcher.add_handler(CommandHandler('start', other_commands.start))
updater.dispatcher.add_handler(CommandHandler('help', other_commands.help))
updater.dispatcher.add_handler(CommandHandler('adminHelp', other_commands.adminHelp))
updater.dispatcher.add_handler(CommandHandler('admins', other_commands.adminList))
updater.dispatcher.add_handler(CommandHandler('identify', other_commands.identify))

# manage suggestions
updater.dispatcher.add_handler(CommandHandler('rollinfo', sheet_commands.rollInfo))
updater.dispatcher.add_handler(CommandHandler('count', sheet_commands.countSuggestions))
updater.dispatcher.add_handler(CommandHandler('add', sheet_commands.addSuggestion))

# Alex mods
updater.dispatcher.add_handler(CommandHandler('russian', other_commands.russian))
updater.dispatcher.add_handler(CommandHandler('ball', other_commands.ball))
updater.dispatcher.add_handler(CommandHandler('today', today.today))
updater.dispatcher.add_handler(CommandHandler('toast', other_commands.toast))

# updater.dispatcher.add_error_handler(other_commands.error_callback)

updater.start_polling()
updater.idle()
