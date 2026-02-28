from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate


# ----------------------------------------------------------------------
# A Flask alkalmazás, az adatbázis-kezelés (SQLAlchemy), a jelszó-hash(Bcrypt) 
# és a bejelentkezés-kezelés (LoginManager) inicializálása és alapbeállításai
# ----------------------------------------------------------------------
app = Flask(__name__)

# --- Adatbázis és konfiguráció beállítása ---
db = SQLAlchemy()
app.config.from_object('config')
db.init_app(app)

# --- Flask-Migrate inicializálása ---
migrate = Migrate(app, db)

# --- Biztonság és autentikáció ---
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.init_app(app)
csrf = CSRFProtect(app)

# --- Flask-Login testreszabása ---
login_manager.login_message = "Az oldal használatához be kell jelentkezned"
login_manager.login_message_category = 'danger'
login_manager.login_view = 'login'


# ----------------------------------------------------------------------
# USER LOADER ÉS IMPORTOK
# - Felhasználó visszatöltése session-ből
# ----------------------------------------------------------------------

""" Flask-Login user_loader függvénye
Ez a függvény felelős azért, hogy a session-ben tárolt user_id alapján
minden kérésnél visszatöltse az aktuálisan bejelentkezett felhasználót.
A Flask-Login automatikusan meghívja (model.py) """

@login_manager.user_loader
def load_user(user_id):
    from application.models import User
    return User.query.get(int(user_id))

# --- Útvonalak (route-ok) betöltése ---
from application import routes
