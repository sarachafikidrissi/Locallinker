""" This is a model that defines the Database"""

from application import db, login_manager
from flask_login import UserMixin

user_services = db.Table('user_services',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id'), primary_key=True)
)

@login_manager.user_loader
def load_user(user_id):
    """ A function that loads and return the user based on user ID """
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """ This is a Class that represents users in the database """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    user_type = db.Column(db.String(20), nullable=False, default='regular') 
    service= db.Column(db.String(20), nullable=False, default='Home Cleaning') 
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    
class Service(db.Model):
    """ This is a Class that represents service in the database """
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())

    providers = db.relationship('User', secondary=user_services, backref=db.backref('services', lazy='dynamic'))


class BookingStatus:
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    CANCELLED = 'Cancelled'

class Booking(db.Model):
    """ This is a Class that represents Booking in the database """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    booking_date = db.Column(db.TIMESTAMP, nullable=False)
    status = db.Column(db.String(50), nullable=False, default=BookingStatus.PENDING)
    user_city = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)  
    task_details = db.Column(db.Text, nullable=False)

class Review(db.Model):
    """ This is a Class that represents review in the database """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
