import datetime, numpy

watb = -1001049406492
newseeds = -1001138132564

devs = list(map(lambda x: x.rstrip('\n'), open('devs_names.txt', 'r').readlines()))
admins = list(map(lambda x: x.rstrip('\n'), open('admins_names.txt', 'r').readlines()))

# time

def getTime():
    return datetime.datetime.now()

def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0

def checkAccess(update):
    value = update.message.from_user.username in admins
    print("checkAccess", value)
    return value

def checkDevAccess(update):
    return update.message.from_user.username in devs

def isNewCommand(update):
    timenow = unix_time_millis(datetime.datetime.now())
    messageTime = unix_time_millis(update.message.date)
    dt = timenow - messageTime
    value = dt < (20000)
    print("isNewCommand", value)
    return value

def isNewSeeds(update):
    return update.message.chat_id == newseeds

def getWeights(count):
    values = list(range(0, count))
    weights = list(map(lambda x: count - x/1.05, values))
    weights = numpy.array(weights)
    weights /= weights.sum()
    return weights