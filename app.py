from flask import Flask, render_template, url_for, request, redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bot
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from message import Message
import json
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mattarchat.db'
app.config['SECRET_KEY'] = 'thisissecret'
app.secret_key = b',\\k+U8\xe4BY\x8f\xf1\xe9?htl'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class Converation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200),nullable=False)
    sessNum = db.Column(db.Integer, nullable=False, default=1)
    userMsg = db.Column(db.String(200),nullable=False)
    botReply = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    def __repr__(self):
        return "<Converation %r>" % self.id

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    reciter = db.Column(db.String(200))
    sessNum = db.Column(db.Integer, nullable=False, default=1)
    def __repr__(self):
        return "<User %r>" % self.username
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

def setReciter(id):
    user = Users.query.filter_by(username=current_user.username).first()
    user.reciter=id
    db.session.commit()

def getReciter():
    user = Users.query.filter_by(username=current_user.username).first()
    return user.reciter

@app.route('/',methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return render_template('login.html')
    else:
        if request.method == 'POST':
            if session.get('ayat') is not None:
                session.pop('ayat',None)
            message = Message(request.form['message'], datetime.now().strftime('%H:%M'), current_user.username)
            if message.text:
                response = Message(bot.reply(current_user.username, message.text), datetime.now().strftime('%H:%M'), 'bot')
                newConv = Converation(user=current_user.username, userMsg=message.text, botReply=response.text,sessNum=current_user.sessNum)
                try:
                    db.session.add(newConv)
                    db.session.commit()
                except:
                    return "Database addition error occurred"
                if session.get('chat') is not None:
                    session['chat'] = session['chat'] + [message.__dict__, response.__dict__]
                else:
                    session['chat'] = [message.__dict__, response.__dict__]
        return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        newUser = Users(username=username,password=password)
        try:
            db.session.add(newUser)
            db.session.commit()
            user = Users.query.filter_by(username=username).first()
            login_user(user)
            return redirect('/')
        except:
            return "Database addition error occurred"
    else:
        return render_template('register.html')

@app.route('/login',methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = Users.query.filter_by(username=username,password=password).first()
    if user == None:
        return render_template('login.html')
    user.sessNum += 1
    db.session.commit()
    login_user(user)
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    session.pop('chat',None)
    session.pop('ayat',None)
    bot.logoutUser(current_user.username)
    logout_user()
    return render_template('login.html')

@app.route('/profile')
@login_required
def profile():
    return "User is " +current_user.username+" and session is "+str(current_user.sessNum)

if __name__ == "__main__":
    app.run(debug=True)
