from core import isNewCommand, checkAccess, isNewSeeds, getTime
from session import saveConfig, loadConfig, send, reply, auth
from utility import fValue, fNonEmpty, fLower

from session_commands import newAlbumSetPosition
from core import getWeights
import numpy, random, time

# countdown

def randomCunt():
    return random.choice(["Ready Lets Go", "Here we go…", 
        "Come to Daddy", "Oh boy, here I go killin' again!", "Prepare your diapers…"])

def cunt(bot, update):
    if not isNewCommand(update): return
    if not checkAccess(update): return 

    message = [1]

    if len(update.message.text.split(" ", 1)) > 1:
        message = update.message.text.split(" ", 1)[1].strip()
    else:
        message = randomCunt()
    send(bot, message)

    count = 5
    while count:
        send(bot, "{}".format(count))
        time.sleep(1)
        count -= 1

    send(bot, "PLAY!")

    config = loadConfig()
    if config['isPlaying'] == True: return

    # also call /new
    if config['lastRoll'] is not None:
        newAlbumSetPosition(bot, config['lastRoll'])

        # newAlbumSetPosition updates config, need to reload it from disk
        config = loadConfig() 
        config['lastRoll'] = None 
        saveConfig(config)

# roll

def getRandom(count):
    values = list(range(0, count))
    weights = getWeights(count)
    return numpy.random.choice(values, p=weights)

def roll(bot, update):
    if not isNewCommand(update): return
    if not checkAccess(update): return

    config = loadConfig()
    if config['isPlaying'] == True:
        reply(update, "Another session is still on. I'm afraid I can't do that.")
        return

    wks = auth()
    suggestionNames = list(filter(fNonEmpty, map(fValue, wks.range('B4:B100'))))
    illegalNames = list(map(fLower, list(filter(fNonEmpty, map(fValue, wks.range('G4:G9'))))))

    values = []
    for i in range(len(suggestionNames)):
        name = suggestionNames[i].lower()
        if name not in illegalNames:
            values.append({"number": i+4, "name": name })       

    validSuggestionsCount = len(values)

    if validSuggestionsCount == 0:
        reply(update, "No suggestions found.")
        return

    # get random (favor older suggestions)
    rolled_from_valid = getRandom(validSuggestionsCount-1)
    result = values[rolled_from_valid]["number"]

    spreadsheetNumber = result
    rolled = list(map(fValue, wks.range('A'+str(spreadsheetNumber) +':E'+ str(spreadsheetNumber))))
    
    config['lastRoll'] = spreadsheetNumber
    saveConfig(config)

    send(bot,
        "<b>Rolled {}</b>\n{} - {} ({})\nSuggested by: {}" .format(
            spreadsheetNumber, rolled[2], 
            rolled[4], rolled[3], 
            rolled[1]), parse_mode="HTML")

# suggest

def suggest(bot, update):
    if not isNewCommand(update): return
    
    config = loadConfig()
    if config['isPlaying'] == False:
        send(bot, "<b>Anyone in for a </b>#musictheatre<b> session?</b>", parse_mode="HTML")
    else:
        send(bot, "Another session is still in place.")
