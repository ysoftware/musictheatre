from core import isNewCommand, checkAccess, isNewSeeds, getTime
from session import saveConfig, loadConfig, send, reply, auth
from utility import fValue, fNonEmpty, fLower

from core import getWeights
import numpy, re

# archive

def archive(bot, update):
    if not isNewCommand(update): return
    if not checkAccess(update): return
    if debug: return # todo move bot to a test sheet

    position = int(update.message.text.split(" ")[1])
    archiveDo(bot, position)
    send(bot, "Suggestion moved to the archive.")
    
def archiveDo(bot, position):
    if debug: return # todo move bot to a test sheet

    wks = auth()
    now = getTime()

    archiveNames = list(filter(fNonEmpty, map(fValue, wks.range('G4:G1000'))))
    suggestionNames = list(filter(fNonEmpty, map(fValue, wks.range('B4:B100'))))
    lastSuggestion = len(suggestionNames) + 4
    archiveLastPosition = len(archiveNames) + 4

    rolledCells = wks.range('B'+str(position)+':E'+ str(position))
    rolled = list(map(fValue, rolledCells))

    # move archive cells down 1 row
    archiveOldCells = wks.range('F4:L'+str(archiveLastPosition+1))
    lenArchiveOld = len(archiveOldCells)
    for i in reversed(range(len(archiveOldCells))):
        if lenArchiveOld > i + 7:
            archiveOldCells[i+7].value = archiveOldCells[i].value

    wks.update_cells(archiveOldCells)

    # move suggestion to F4
    archiveCells = wks.range('F4:L4')
    archiveCells[0].value = now.strftime("%d %b %y")
    archiveCells[1].value = rolled[0]
    archiveCells[2].value = rolled[1]
    archiveCells[3].value = rolled[2]
    archiveCells[4].value = rolled[3]
    archiveCells[5].value = ""
    archiveCells[6].value = ""

    wks.update_cells(archiveCells)

    # move suggestions up 1 row
    suggestionCells = wks.range('B'+str(position)+':E'+str(lastSuggestion))
    lenSuggestionCells = len(suggestionCells)
    for i in range(len(suggestionCells)):
        if lenSuggestionCells > i + 4:
            suggestionCells[i].value = suggestionCells[i+4].value

    wks.update_cells(suggestionCells)

# manage suggestions

def countSuggestions(bot, update):
    if not isNewCommand(update): return

    array = update.message.text.split(" ")
    if len(array) < 2:
        reply(update, "Enter the name to see how many albums he has suggested.")
        return

    name = update.message.text.split(" ")[1]
    wks = auth()

    originalRows = list(map(fValue, wks.range('B4:B100')))
    foundRows = list(filter(lambda value: value.lower() == name.lower(), originalRows))
    suggestionsCount = len(foundRows)

    originalArchive = list(map(fValue, wks.range('G4:G1000')))
    foundArchive = list(filter(lambda value: value.lower() == name.lower(), originalArchive))
    archiveCount = len(foundArchive)

    if suggestionsCount > 0:
        if archiveCount > 0:
            reply(update, "{} current suggestions by {}. Also {} in archive.".format(
                suggestionsCount, foundRows[0], archiveCount))
        else :
            reply(update, "{} current suggestions by {}.".format(
                suggestionsCount, foundRows[0]))
    elif archiveCount > 0:
        reply(update, "No current suggestion by {} but there are {} in archive.".format(
            foundArchive[0]))
    else:
        reply(update, "No such thing.")

def addSuggestion(bot, update):
    if debug: return # todo move bot to a test sheet
    
    if not isNewCommand(update): return

    array = re.split("[;\n]", update.message.text)

    if len(array) != 4:
        reply(update, "Enter suggester name, artist, year and title of release (use semicolon or new line to divide input)\nLike this: \"Yaro; Pink Floyd; The Dark Side of the Moon; 1973\"")
        return

    wks = auth()
    
    # name artist year album
    name = array[0].strip()[5:]
    artist = array[1].strip()
    album = array[2].strip()
    year = int(array[3].strip())

    if year > 2020 or year < 1900:
        reply(update, "Wrong year")
        return
    
    suggestionNames = list(filter(fNonEmpty, map(fValue, wks.range('B4:B100'))))
    foundRows = list(filter(lambda value: value.lower() == name.lower(), suggestionNames))

    if len(foundRows) >= 5:
        reply(update, "This one already has enough suggestions.")
        return

    newSuggestion = len(suggestionNames) + 4

    # add suggestion
    newCells = wks.range('B'+str(newSuggestion)+':E'+str(newSuggestion))
    newCells[0].value = name
    newCells[1].value = artist
    newCells[2].value = year
    newCells[3].value = album

    wks.update_cells(newCells)

    reply(update, "{} by {} ({}) is now suggested by {}.".format(
        album, artist, year, name))


def rollInfo(bot, update):
    if not isNewCommand(update): return

    wks = auth()

    suggestions = list(filter(fNonEmpty, map(fValue, wks.range('B4:B100'))))
    count = len(suggestions)

    if count < 2: return

    values = getWeights(count)

    array = update.message.text.split(" ")
    if len(array) > 1:
        try: 
            position = int(array[1])
            prob = values[position - 4] * 100
            reply(update, "Probability of rolling {0} is {1:.1f}%".format(position, prob))
            return
        except Exception as e: print(e)

    first = values[0] * 100
    last = values[-1] * 100
    reply(update, "Roll probability (linear distribution):\nOldest: {0:.1f}%\nNewest: {1:.1f}%".format(first, last))
