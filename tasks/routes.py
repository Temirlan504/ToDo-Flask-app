from flask import render_template
from tasks import app

@app.route('/')
def home():
    return render_template('index.html', title='My App')

@app.route('/login')
def login():
    return render_template('login.html', title='Login')

@app.route('/register')
def register():
    return render_template('register.html', title='Register')
