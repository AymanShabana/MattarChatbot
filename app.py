from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bot
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mattarchat.db'
app.config['SECRET_KEY'] = 'thisissecret'
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
    def __repr__(self):
        return "<User %r>" % self.username
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route("/chat", methods=["POST"])
def chat():
    if request.method == 'POST':
        userMsg = request.form['content']
        botReply = bot.chat(userMsg)
        newConv = Converation(user=current_user.username,userMsg=userMsg,botReply=botReply)
        try:
            db.session.add(newConv)
            db.session.commit()
            return redirect('/')
        except:
            return "Database addition error occurred"

@app.route('/',methods=['GET'])
def index():
    user = Users.query.filter_by(username='ayman').first()
    login_user(user)
    chat = Converation.query.order_by(Converation.date_created).all()
    #return render_template('index.html',chat=chat)
    return render_template('login.html')

@app.route('/register',methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']



@app.route('/logout')
@login_required
def logout():
    logout_user()
    chat = Converation.query.order_by(Converation.date_created).all()
    return render_template('index.html',chat=chat)

@app.route('/profile')
@login_required
def profile():
    return "User is " +current_user.username

if __name__ == "__main__":
    app.run(debug=True)