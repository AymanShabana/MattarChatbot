from rivescript import RiveScript

bots={}


def createInstance(username):
    bots[username] = RiveScript()
    bots[username].load_directory("./brain")
    bots[username].sort_replies()

def removeInstance(username):
    bots.pop(username)

def checkInstance(username):
    return username in bots

def chat(message,username):
    if not username in bots:
        bots[username] = RiveScript()
        bots[username].load_directory("./brain")
        bots[username].sort_replies()
    if message == "":
        return "Send me a proper message"
    reply = bots[username].reply("user", message)
    return reply
