from rivescript import RiveScript

bot = RiveScript(utf8=True)
bot.load_directory('brain')
bot.sort_replies()

while True:
    message = input('You: ')
    print('Bot:', bot.reply('User', message))
