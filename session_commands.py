from core import isNewCommand, checkAccess, isNewSeeds, getTime, debug
from session import saveConfig, loadConfig, send, reply, auth
from utility import fValue, fNonEmpty, fLower

from sheet_commands import archiveDo
import numpy

# session

def over(bot, update):
    if not checkAccess(update): return

    config = loadConfig()
    if config['isPlaying'] == True:
        if isNewCommand(update):
            send(bot, "#musictheatre it's OVER.")
        endSession()
    else:
        reply(update, "You betcha it is.")

def abort(bot, update):
    if not checkAccess(update): return

    config = loadConfig()
    if config['isPlaying'] == True:
        endSession()

        if isNewCommand(update):

            if debug: 
                send(bot, "#musictheatre it's ABORTED. (not really)")
                return # todo move bot to a test sheet

            send(bot, "#musictheatre it's ABORTED.")

            # add 'aborted'
            wks = auth()
            archiveCells = wks.range('F4:L4')
            if archiveCells[4].value == config['album']:
                archiveCells[6].value = "aborted"
                wks.update_cells(archiveCells)
    else:
        reply(update, "I'll abort you, you fucking bitch.")

def newAlbum(bot, update):
    if not isNewCommand(update): return
    if not checkAccess(update): return

    message = update.message.text.split(" ", 1)[1].strip()

    # new artist - album
    if " - " in message:
        artistName = message.split(" - ", 1)[0].strip()
        albumName = message.split(" - ", 1)[1].strip()
        newAlbumSet(bot, config, artistName, albumName, None, None)
    # new {number}
    else:
        newAlbumSetPosition(bot, message)

def newAlbumSetPosition(bot, position):
    config = loadConfig()
    if config['isPlaying'] == False:
       if int(position) >= 4:
            wks = auth()
            info = list(map(fValue, wks.range("B{0}:E{0}".format(position, position))))
            newAlbumSet(bot, config, info[1], info[3], info[2], info[0])
            
            # archive as well
            archiveDo(bot, position)
    else:
        send(bot, "We're still in session.")

def newAlbumSet(bot, config, artistName, albumName, year, suggested):
    config['isPlaying'] = True
    config['artist'] = artistName
    config['album'] = albumName
    config['track'] = ""

    text = ""
    if year is not None and suggested is not None:
        config['year'] = year
        config['suggested'] = suggested

        text = "#musictheatre New Album: {0} - {1} ({2}) [Suggested by: {3}]".format(
            config['artist'], config['album'], config['year'], config['suggested'])
    else:
        text = "#musictheatre New Album: {0} - {1}".format(
            config['artist'], config['album'])

    send(bot, text)
    saveConfig(config)

def nextSong(bot, update):
    if not isNewCommand(update): return
    if not checkAccess(update): return

    config = loadConfig()
    if config['isPlaying'] == True:
        trackName = update.message.text.split(" ", 1)[1].strip()
        if len(trackName) > 0 and len(config['artist']) > 0 and trackName != config['track']:
            config['track'] = trackName
            text = "#musictheatre {0} - {1}".format(
                config['artist'], config['track'])
            send(bot, text)
            saveConfig(config)
    else:
        send(bot, "What album was that again?")

def endSession():
    config = loadConfig()
    config.pop('artist', None)
    config.pop('track', None)
    config.pop('album', None)
    config.pop('suggested', None)
    config.pop('year', None)
    config['isPlaying'] = False
    saveConfig(config)

# current

def currentAlbum(bot, update):
    if not isNewCommand(update): return

    config = loadConfig()
    if config['isPlaying'] == True:
        if len(config['artist']) > 0 and len(config['album']) > 0:
            text = "{0} by {1}".format(
                config['album'], config['artist'])
            if config['year'] is not None:
                text += " ({})".format(config['year'])
            if config['suggested'] is not None:
                text += " [Suggested by: {}]".format(
                    config['suggested'])
            reply(update, text)
    else:
        reply(update, "Nothing is playing.")


def currentTrack(bot, update):
    if not isNewCommand(update): return
    
    config = loadConfig()
    if config['isPlaying'] == True:
        if len(config['artist']) > 0 and len(config['album']) > 0 and len(config['track']) > 0:
            text = "Now playing: {0} - {1} (from {2})".format(
                config['artist'], config['track'], 
                config['album'])
            reply(update, text)
    else:
        reply(update, "Nothing is playing.")
