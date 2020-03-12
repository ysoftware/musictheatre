from core import isNewCommand, checkAccess, isNewSeeds, getTime
from session import saveConfig, loadConfig, send, reply, auth
from utility import fValue, fNonEmpty, fLower

from session_commands import newAlbumSetPosition
from core import getWeights
import numpy, random, time

# countdown

def randomCunt():
    return random.choice(["Ready Lets Go", "Here we go...", 
        "Come to Daddy", "Oh boy, here I go killin' again!"])

def cunt(bot, update):
    if not isNewCommand(update):
        return
    if checkAccess(update):
        message = [1]

        if len(update.message.text.split(" ", 1)) > 1:
            message = update.message.text.split(" ", 1)[1].strip()
        else:
            message = randomCunt()
        send(bot, message.encode('utf-8'))

        count = 5
        while count:
            send(bot, "{}".format(count))
            time.sleep(1)
            count -= 1

        send(bot, "PLAY!")

        # also call /new
        config = loadConfig()
        if config['lastRoll'] is not None:
            newAlbumSetPosition(bot, config['lastRoll'])
            config['lastRoll'] = None 
            saveConfig(config)

# roll

def getRandom(count):
    values = list(range(0, count))
    weights = getWeights(count)
    return numpy.random.choice(values, p=weights)

def roll(bot, update):
    if not isNewCommand(update):
        return
    if not checkAccess(update):
        return
    config = loadConfig()

    if config['isPlaying'] == False:

        wks = auth()
        suggestionNames = filter(fNonEmpty, map(fValue, wks.range('B4:B100')))
        illegalNames = map(fLower, filter(fNonEmpty, map(fValue, wks.range('G4:G9'))))
        suggestionsCount = len(suggestionNames)

        values = []
        for i in range(4, len(suggestionNames)):
            name = suggestionNames[i]
            if not name in illegalNames:
                values.append({"number": i+4, "name": suggestionNames })    

        pr = ""
        for s in values:
            pr += str(s["number"]) + " " + s["name"] + "\n"
        reply(update, pr)

        return

        if suggestionsCount > 0:
            for _ in range(5):

                # get random (favor older suggestions)
                result = getRandom(suggestionsCount-1)

                spreadsheetNumber = result + 4
                rolled = map(fValue, wks.range('A'+str(spreadsheetNumber)
                    +':E'+ str(spreadsheetNumber)))
                if not rolled[1].lower() in illegalNames:
                    config['lastRoll'] = spreadsheetNumber
                    saveConfig(config)

                    send(bot,
                        "<b>Rolled {}</b>\n{} - {} ({})\nSuggested by: {}" .format(
                            spreadsheetNumber, rolled[2].encode('utf-8'), 
                            rolled[4].encode('utf-8'), rolled[3].encode('utf-8'), 
                            rolled[1].encode('utf-8')), parse_mode="HTML")
                    return
                else:
                    send(bot,
                        "Rolled {}. {} - illegal.".format(
                            spreadsheetNumber, rolled[1].encode('utf-8')))
        else:
            reply(update, "No suggestions found.")
    else:
        reply(update, "Another session is still on. I'm afraid I can't do that.")

# suggest

def suggest(bot, update):
    if not isNewCommand(update):
        return
    config = loadConfig()
    if config['isPlaying'] == False:
        send(bot, "<b>Anyone in for a </b>#musictheatre<b> session?</b>", parse_mode="HTML")
    else:
        send(bot, "Another session is still in place.")
