import numpy, sys
from datetime import datetime, timezone

watb = -1001049406492
newseeds = -1001138132564
bot_test = -329730756

devs = list(map(lambda x: x.rstrip('\n'), open('./env/devs_names.txt', 'r').readlines()))
admins = list(map(lambda x: x.rstrip('\n'), open('./env/admins_names.txt', 'r').readlines()))

def checkIfDebug():
    for arg in sys.argv:
        if arg == "-debug":
            return True
    return False
debug = checkIfDebug()

def getTime():
    return datetime.now()

def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0)
    diff = dt.replace(tzinfo=None) - epoch
    return diff.total_seconds() * 1000.0

def checkAccess(update):
    value = update.message.from_user.username in admins
    return value

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def checkDevAccess(update):
    return update.message.from_user.username in devs

def isNewCommand(update):
    timenow = unix_time_millis(getTime())
    messageTime = unix_time_millis(utc_to_local(update.message.date))
    dt = timenow - messageTime
    value = dt < (20000)
    return value

def main_channel(): 
    if debug: return bot_test
    else: return newseeds

def isNewSeeds(update):
    return update.message.chat_id == main_channel()

def getWeights(count):
    values = list(numpy.arange(0.0, count))
    weights = list(map(lambda x: (count-x) ** 5, values))
    weights = numpy.array(weights)
    weights /= weights.sum()
    return weights