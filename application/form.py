""" This is a model that defines Forms"""

# Import necessary modules and classes from Flask and WTForms
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import User

# Registration Form
class RegistrationForm(FlaskForm):
    """ A class that defines form fields using WTForms and provide
        Validators for each field
    """
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('User Type', choices=[('regular', 'Regular'), ('provider', 'Provider')], validators=[DataRequired()])
    service = SelectField('Your Primary Service', choices=[('home cleaning' ,'Home Cleaning'), ('plumbing' ,'plumbing'), ('general handyman' ,'General Handyman'), ('event planning' ,'Event Planning'), ('assembly' ,'Assembly'), ('electrical' ,'Electrical')], validators=[DataRequired()])
    

    submit = SubmitField('Sign up')

    def validate_username(self, username):
        """A function that Validate username
        and check if the username is already taken
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose different one.')
    
    def validate_email(self, email):
        """ A function that validate email and check if already registered """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose different one.')

# Login Form
    
class LoginForm(FlaskForm):
    """ A class that define form fields for login form """
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Rememebr Me')

    submit = SubmitField('Login')

    
# Update user profile Form
class UpdateAccountForm(FlaskForm):
    """ A class that defines form fields using WTForms and provide
        Validators for each field
    """
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        """A function that Validate username
        and check if the username is already taken
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose different one.')
            
    def validate_email(self, email):
        """ A function that validate email and check if already registered """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose different one.')
            
class UpdateProviderAccountForm(FlaskForm):
    """ A class that defines form fields using WTForms and provide
        Validators for each field
    """
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    service = SelectField('Your Primary Service', choices=[('home cleaning' ,'Home Cleaning'), ('plumbing' ,'plumbing'), ('general handyman' ,'General Handyman'), ('event planning' ,'Event Planning'), ('assembly' ,'Assembly'), ('electrical' ,'Electrical')], validators=[DataRequired()])

    submit = SubmitField('Update')

    def validate_username(self, username):
        """A function that Validate username
        and check if the username is already taken
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose different one.')
            
    def validate_email(self, email):
        """ A function that validate email and check if already registered """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose different one.')