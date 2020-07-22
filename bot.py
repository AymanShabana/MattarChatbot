from rivescript import RiveScript

bot = RiveScript()
bot.load_directory("./brain")
bot.sort_replies()

def chat(message,username):
    if message == "":
        return "Send me a proper message"
    reply = bot.reply(username, message)
    return reply
