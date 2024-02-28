from flask import Blueprint, render_template, url_for, flash, redirect
from form import RegistrationForm, LoginForm

views = Blueprint(__name__, "home")



@views.route('/')
def home():
    return render_template('index.html')

@views.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('views.home'))
    return render_template('register.html', title='Register', form=form)

@views.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('views.home'))
        else:
            flash('Login Unseccessful, Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)