from flask import Flask, render_template, request, session
from bot import reply
from message import Message

app = Flask('__name__')
app.secret_key = b',\\k+U8\xe4BY\x8f\xf1\xe9?htl'

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        message = Message(request.form['message'], '10:00', 'user')
        if message.text:
            response = Message(reply('User', message.text), '10:00', 'bot')
            if session.get('chat') is not None:
                session['chat'] = session['chat'] + [message.__dict__, response.__dict__]
            else:
                session['chat'] = [message.__dict__, response.__dict__]
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
