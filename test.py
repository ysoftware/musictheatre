import sys

def checkIfDebug():
    for arg in sys.argv:
        if arg == "-debug":
            return True
    return False

print(checkIfDebug())