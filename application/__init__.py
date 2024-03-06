from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '020290d9aee6f0287ebfb4b50924bd7d53c582e331668f5984c2355cc8abc8cd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locallinker.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


from application import views