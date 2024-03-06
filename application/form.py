from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import User

# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('User Type', choices=[('regular', 'Regular'), ('provider', 'Provider')], validators=[DataRequired()])
    service = SelectField('Your Primary Service', choices=[('home cleaning' ,'Home Cleaning'), ('plumbing' ,'plumbing'), ('handy man' ,'Handy man'), ('event planning' ,'Event Planning'), ('assembly' ,'Assembly'), ('electrical' ,'Electrical')], validators=[DataRequired()])
    

    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose different one.')

# Login Form
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Rememebr Me')

    submit = SubmitField('Login')
