import os
import secrets
# from PIL import Image
from flask import render_template, url_for, flash, redirect, session, request
from sqlalchemy import func
from application import app, db, bcrypt
from application.form import RegistrationForm, LoginForm, UpdateAccountForm , UpdateProviderAccountForm
from application.models import User, Service, Booking, Review, user_services, Booking
from flask_login import login_user, current_user, logout_user, login_required
from urllib.parse import unquote
from datetime import datetime
# import logging

# logging.basicConfig(filename='app.log', level=logging.DEBUG)



# Dictionary containing service data
services_data = {
    "Home Cleaning": {
        "provider_id": None,
        "title": "Home Cleaning",
        "description": "Professional home cleaning services including bedroom cleaning, home cleaning, and housekeeping.",
        "price": 50.00,
        "sub_services": ["Bedroom Cleaning", "Home Cleaning", "Housekeeping"]
    },
    "Plumbing": {
        "provider_id": None,
        "title": "Plumbing",
        "description": "Professional plumbing services including drain repair, toilet repair, and unclog toilet.",
        "price": 75.00,
        "sub_services": ["Drain Repair", "Toilet Repair", "Unclog Toilet"]
    },
    "Event Planning": {
        "provider_id": None,
        "title": "Event Planning",
        "description": "Professional event planning services including wedding planner, DJ services, and event marketer.",
        "price": 100.00,
        "sub_services": ["Wedding Planner", "DJ Services", "Event Marketer"]
    },
    "Assembly": {
        "provider_id": None,
        "title": "Assembly",
        "description": "Professional assembly services including desk assembly, furniture assembly, and grill assembly.",
        "price": 60.00,
        "sub_services": ["Desk Assembly", "Furniture Assembly", "Grill Assembly"]
    },
    "Electrical": {
        "provider_id": None,
        "title": "Electrical",
        "description": "Professional electrical services including light switch installation, outlet installation, and light fixtures.",
        "price": 80.00,
        "sub_services": ["Light Switch Installation", "Outlet Installation", "Light Fixtures"]
    },
    "General Handyman": {
        "provider_id": None,
        "title": "General Handyman",
        "description": "Professional handyman services including handy helper, locks installation, and TV mounting.",
        "price": 70.00,
        "sub_services": ["Handy Helper", "Locks Installation", "TV Mounting"]
    }
}

def add_services_to_database():
    """ This is a function that add services to the database 
    if the don't already exist"""
    for service_name, service_info in services_data.items():
        # Check if the service already exists in the database
        existing_service = Service.query.filter_by(title=service_name).first()
        if existing_service is None:
            # Service does not exist, so add it to the database
            service = Service(
                title=service_name,
                description=service_info["description"],
                price=service_info["price"]
                
            )
            db.session.add(service)
    db.session.commit()

# Execute the function within the application context to add services to the database
with app.app_context():
    add_services_to_database()

# Route for the home page
@app.route('/')
@app.route('/home')
def home():
    """ This is a function that redirect user to home page """
    return render_template('index.html')

# Route and function for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    """ this is a function for to register user
        redirect user to home page if he logged
        otherwise to register page """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
         # Hash the password before storing it in the database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_type = form.user_type.data
        if user_type not in ['regular', 'provider']:
            flash('Invalid user type', 'error')
            return redirect(url_for('register'))
        user_service = form.service.data
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, user_type=user_type, service=user_service)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You ar now able to log in', 'success')

        # If the registered user is a provider, update the provider_id in the Service table
        if user.user_type == 'provider':
            service = Service.query.filter(func.lower(Service.title) == user_service).first()
            if service:
                user_service_entry = user_services.insert().values(user_id=user.id, service_id=service.id)
                db.session.execute(user_service_entry)
                db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Route and function for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """ This is a function for user login """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            session['user_id'] = user.id
            if user.user_type == 'regular':
                return redirect(next_page) if next_page else redirect(url_for('user_dashboard'))
            elif user.user_type == 'provider':
                return redirect(url_for('provider_dashboard'))
            flash('Login successful', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unseccessful, Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# Route and function for user logout
@app.route('/logout')
def logout():
    """ This is a function for user logout """
    logout_user()
    session.pop('user_id', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)

    return picture_fn
# Route and function for user account
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """This is a function that redirect user to it's profile """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        # logging.info(f'Form submitted - Username: {form.username.data}, Email: {form.email.data}')
        return redirect(url_for('account'))
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route('/provider_ccount', methods=['GET', 'POST'])
@login_required
def provider_account():
    """This is a function that redirect user to it's profile """
    form = UpdateProviderAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.service = form.service.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('provider_account'))
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('provider_account.html', title='Account', image_file=image_file, form=form)

# Route and function for regular user dashboard
@app.route('/user_dashboard', methods=['GET', 'POST'])
def user_dashboard():
    """ This is a function that redirect regular user to his/her dashboard """
    if request.method == 'POST':
        selected_service = request.form.get('input')
        # logging.debug('Selected Service: %s', selected_service)
        return redirect(url_for('booking_form', service=selected_service))
    return render_template('user_dashboard.html', title='Dashboard')

# Route and function for provider dashboard
@app.route('/provider_dashboard',  methods=['GET', 'POST'])
def provider_dashboard():
    """ This is a function that redirect provider  to his/her dashboard """
    return render_template('provider_dashboard.html', title='Dashboard')

# Route and function for service page
@app.route('/services')
def services():
    """ This is a function that redirect user to service page"""
    services = Service.query.all()
    return render_template('services.html', title='Services', services=services, service_list=services_data)

@app.route('/book/<service>', methods=['GET', 'POST'])
def booking_form(service):
    decoded_service = unquote(service)
    # logging.debug('Decoded Service: %s', decoded_service)
    inputed_service = Service.query.filter((Service.title) == decoded_service).first()
    # logging.debug('Inputed Service: %s', inputed_service)
    if inputed_service:
        inputed_service_id= inputed_service.id
        # logging.debug('Decoded Service: %s', inputed_service_id)
    # get user_id of service provider:
    user_ids = db.session.query(User.id).join(User.services).filter(Service.id == inputed_service_id).all()
    user_ids_list = [user_id[0] for user_id in user_ids]
    # logging.debug('service_provider_id: %s', user_ids_list)
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        city = request.form.get('city')
        email = request.form.get('email')
        task_summary = request.form.get('description')
        booking_date = datetime.now()

        # Create new Booking instance
        new_booking = Booking(
            user_id = current_user.id,
            service_id = inputed_service_id,
            user_city = city,
            phone_number = phone_number,
            email = email,
            task_summary = task_summary,
            booking_date = booking_date
        )
        db.session.add(new_booking)
        db.session.commit()
    return render_template('booking_form.html', title='Booking', service=decoded_service)
