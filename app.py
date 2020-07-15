from rivescript import RiveScript
import sqlite3
import arrow

#db = sqlite3.connect('attendance.db')
#c = db.cursor()
#c.execute('''DROP TABLE attendance''')
#db.commit()
#c.execute('''CREATE TABLE attendance
#             (name text, year text, date DATE)''')
#c.execute("INSERT INTO attendance VALUES ('Essam H','Junior','"+str(arrow.now().format('YYYY-MM-DD'))+"')")
#db.commit()
#t = ('Essam H',)
#c.execute("SELECT * FROM attendance WHERE name=? AND date='"+str(arrow.now().format('YYYY-MM-DD'))+"'", t)
#print(c.fetchone())
#t = ('Ayman Yasser',)
#c.execute("SELECT * FROM attendance WHERE name=? AND date='"+str(arrow.now().format('YYYY-MM-DD'))+"'", t)
#print(c.fetchone())
#db.close()

bot = RiveScript()
bot.load_directory("./brain")
bot.sort_replies()

while True:
    msg = input('You> ')
    if msg == '/quit':
        quit()

    reply = bot.reply("localuser", msg)
    print('Bot>', reply)
