from rivescript import RiveScript

bot = RiveScript(utf8=True)
bot.load_directory('brain')
bot.sort_replies()

def reply(user, message):
    return bot.reply(user, message)

def logoutUser(user):
    try:
        bot.clear_uservars(user)
    except:
        print("User not found")
