import datetime

watb = -1001049406492
newseeds = -1001138132564

admins = [
          "Xanes",
          "ysoftware",
          "tbshfmn",
          "sexy_nutella_69",
          "amobishoproden",
          "jntn7",
          "Doomgoat",
          "Tom_veldhuis",
          "FkinTag"
          ]

# time

def getTime():
    return datetime.datetime.now()

def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0

def checkAccess(update):
    return update.message.from_user.username in admins

def isNewCommand(update):
    timenow = unix_time_millis(datetime.datetime.now())
    messageTime = unix_time_millis(update.message.date)
    dt = timenow - messageTime
    return dt < (20000)

def isNewSeeds(update):
    return update.message.chat_id == newseeds

def getWeights(count):
    values = list(range(0, count))
    weights = list(map(lambda x: count - x/1.05, values))
    weights = numpy.array(weights)
    weights /= weights.sum()
    return weights
