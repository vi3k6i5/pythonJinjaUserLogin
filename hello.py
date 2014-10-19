from flask import Flask, url_for, redirect, request, session
from flask import render_template
from pymongo import MongoClient
import sys

client = MongoClient('localhost', 27017)
db = client['myservice']

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        res = db.myservice.find_one({"user": request.form['username'], "password" : request.form['password']})
        if res:
            session['username'] = request.form['username']
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('login'))
    else:
        if 'username' in session:
            return redirect(url_for('profile'))
        else:
            return render_template('login.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html', name=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        res = db.myservice.find_one({"user": request.form['username']})
        if res:
            return redirect(url_for('login'))
        else:
            db.myservice.insert( { "user": request.form['username'], "password": request.form['password'] } )
            return redirect(url_for('login'))
    else:
        if 'username' in session:
            return redirect(url_for('profile'))
        else:
            return render_template('register.html')

with app.test_request_context():
    print url_for('index')
    print url_for('login')
    print url_for('profile')
    print url_for('logout')
    print url_for('register')

if __name__ == '__main__':
    print "Initializing..."
    print "checking db myservice [Creating db if not exists]..."
    res = db.myservice.find_one({"user": "user@gmail.com"})
    if not res:
        print "creating default user with username user@gmail.com and password as password"
        db.myservice.insert( { "user": "user@gmail.com", "password": "password" } )
    else:
        print "default user exists"
    print "Initialized"
    # set the secret key.  keep this really secret:
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.debug = True
    app.run()