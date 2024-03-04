from flask import render_template, url_for, flash, redirect, session, request
from application import app, db, bcrypt
from application.form import RegistrationForm, LoginForm
from application.models import User, Service, Booking, Review
from flask_login import login_user, current_user, logout_user





@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_type = form.user_type.data
        if user_type not in ['regular', 'provider']:
            flash('Invalid user type', 'error')
            return redirect(url_for('register'))
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, user_type=user_type)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You ar now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            session['user_id'] = user.id
            if user.user_type == 'regular':
                return redirect(url_for('user_dashboard'))
            elif user.user_type == 'provider':
                return redirect(url_for('provider_dashboard'))
            flash('Login successful', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unseccessful, Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    session.pop('user_id', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))

@app.route('/user_dashboard', methods=['GET', 'POST'])
def user_dashboard():
    return render_template('user_dashboard.html', title='Dashboard')

@app.route('/provider_dashboard',  methods=['GET', 'POST'])
def provider_dashboard():
    return render_template('provider_dashboard.html', title='Dashboard')

@app.route('/services')
def services():
    return render_template('services.html', title='Services')
