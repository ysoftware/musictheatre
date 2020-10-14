import datetime, numpy, sys

watb = -1001049406492
newseeds = -1001138132564
bot_test = -329730756

devs = list(map(lambda x: x.rstrip('\n'), open('devs_names.txt', 'r').readlines()))
admins = list(map(lambda x: x.rstrip('\n'), open('admins_names.txt', 'r').readlines()))

def checkIfDebug():
    for arg in sys.argv:
        if arg == "-debug":
            return True
    return False
debug = checkIfDebug()

def getTime():
    return datetime.datetime.now()

def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0

def checkAccess(update):
    value = update.message.from_user.username in admins
    return value

def checkDevAccess(update):
    return update.message.from_user.username in devs

def isNewCommand(update):
    timenow = unix_time_millis(datetime.datetime.now())
    messageTime = unix_time_millis(update.message.date)
    dt = timenow - messageTime
    value = dt < (20000)
    return value

def main_channel(): 
    if debug: return bot_test
    else: return newseeds

def isNewSeeds(update):
    return update.message.chat_id == main_channel()

def getWeights(count):
    values = list(range(0, count))
    best_change = float(2.9)
    step = best_change / count
    weights = list(map(lambda x: (count-x) * step, values))
    weights = numpy.array(weights)
    weights /= count
    return weights