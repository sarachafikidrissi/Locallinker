from flask import Flask
from views import views
app = Flask(__name__)

app.config['SECRET_KEY'] = '020290d9aee6f0287ebfb4b50924bd7d53c582e331668f5984c2355cc8abc8cd'
app.register_blueprint(views, url_prefix="/home")

if __name__ == '__main__':
    app.run(debug=True, port=5000)