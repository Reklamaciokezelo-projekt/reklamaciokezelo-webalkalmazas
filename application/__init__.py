from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# A Flask alkalmazás, az adatbázis-kezelés (SQLAlchemy), a jelszó-hash(Bcrypt) 
# és a bejelentkezés-kezelés (LoginManager) inicializálása és alapbeállításai
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

# betölti a route-okat, hogy a Flask tudja, milyen URL-eket kezeljen
from application import routes

# Adatbázis-táblák létrehozása
with app.app_context():
    db.create_all()