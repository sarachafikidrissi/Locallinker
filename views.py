from flask import Blueprint, render_template

views = Blueprint(__name__, "home")

@views.route('/')
@views.route('/home')
def home():
    return render_template('index.html')