from rivescript import RiveScript


bot = RiveScript()
bot.load_directory("./brain")
bot.sort_replies()

def chat(message):
    #msg = input('You> ')
    #if msg == '/quit':
        #quit()
    if message == "":
        return "Send me a proper message"
    reply = bot.reply("user", message)
    return reply
    #print('Bot>', reply)