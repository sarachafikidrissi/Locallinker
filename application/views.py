from flask import render_template, url_for, flash, redirect
from application import app, db, bcrypt
from application.form import RegistrationForm, LoginForm
from application.models import User, Service, Booking, Review
from flask_login import login_user, current_user, logout_user



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



with app.app_context():
    add_services_to_database()

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
        user_service = form.service.data
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, user_type=user_type, service=user_service)
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
    services = Service.query.all()
    return render_template('services.html', title='Services', services=services, service_list=services_data)


