from application import db, login_manager
from flask_login import UserMixin


# Flask-Login: betölt egy felhasználót az ID alapján
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ----------------------------------------------------------------------
# USER OSZTÁLY
# ----------------------------------------------------------------------
class User(db.Model, UserMixin):
    __tablename__ = 'users' # táblanév

    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(50), nullable=False)
    forename = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(30), nullable=False)

    # Az adott osztály reprezentációja
    def __repr__(self):
        return f"User ({self.username}, {self.email})"