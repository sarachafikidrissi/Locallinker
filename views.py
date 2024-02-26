from flask import Blueprint, render_template, url_for

views = Blueprint(__name__, "home")

@views.route('/')
@views.route('/home')
def home():
    return render_template('index.html')

@views.route('/register')
def register():
    return render_template('register.html')

@views.route('/login')
def login():
    return render_template('login.html')