from app import app
from flask import render_template

@app.route('/homepage')
def homepage():
    return "Hello world"
@app.route('/')
@app.route('/login')
def Login():
    return render_template('login.html')

@app.route('/signup')
def Signup():
    return render_template('signup.html')