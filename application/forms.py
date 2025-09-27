from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import User


class NewUserForm(FlaskForm):
    username = StringField('Név', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('E-mail cím', validators=[DataRequired(), Email(message="A megadott email cím formailag nem megfelelő")])
    password = PasswordField('Jelszó', validators=[DataRequired()])
    confirm_password = PasswordField('Jelszó még egyszer', validators=[DataRequired(), EqualTo('password', message="Nem egyezik a fent megadott jelszóval")])
    submit = SubmitField('Mentés')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Ez a felhasználónév már foglalt, adjon meg másikat")
        # ez a funkció ellenőrzi, hogy van-e már ilyen felhasználónév

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Ez az email cím már foglalt, adjon meg másikat")
        

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Jelszó', validators=[DataRequired()])
    remember = BooleanField('Bejelentkezve maradok')
    submit = SubmitField('Bejelentkezés')