from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
db = SQLAlchemy()
app.config.from_object('config')
db.init_app(app)
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "Az oldal használatához be kell jelentkezned"
login_manager.login_message_category = 'danger'
login_manager.login_view = 'login'

from application import routes

with app.app_context():
    db.create_all()