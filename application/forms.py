from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import User


# Új felhasználó
class NewUserForm(FlaskForm):
    username = StringField('Név', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('E-mail cím', validators=[DataRequired(), Email(message="A megadott email cím formailag nem megfelelő")])
    password = PasswordField('Jelszó', validators=[DataRequired()])
    confirm_password = PasswordField('Jelszó még egyszer', validators=[DataRequired(), EqualTo('password', message="Nem egyezik a fent megadott jelszóval")])
    submit = SubmitField('Mentés')

    # ez a metódus ellenőrzi, hogy van-e már ilyen felhasználónév
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Ez a felhasználónév már foglalt, adjon meg másikat")
        
    # ez a metódus ellenőrzi, hogy foglalt-e már a megadott mail cím
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Ez az email cím már foglalt, adjon meg másikat")
        

# Bejelentkezés
class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Jelszó', validators=[DataRequired()])
    remember = BooleanField('Bejelentkezve maradok')
    submit = SubmitField('Bejelentkezés')


# Felhasználói adatok módosítása (név, email)
class UpdateAccountForm(FlaskForm):
    username = StringField('Név', validators=[DataRequired(), Length(min=2,max=20)])
    submit = SubmitField('Változtatások mentése')
    cancel = SubmitField('Mégse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and user.id != self.original_user.id:
            raise ValidationError("Ez a felhasználónév már foglalt, adjon meg másikat")

# Felhasználói adatok módosítása (jelszó)
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Jelenlegi jelszó', validators=[DataRequired()])
    new_password = PasswordField('Új jelszó', validators=[DataRequired()])
    confirm_password = PasswordField('Új jelszó megerősítése', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Mentés')
    cancel = SubmitField('Mégse')


# Felhasználói fiók törlése
class DeleteAccountForm(FlaskForm):
    password = PasswordField('Jelszó megerősítése', validators=[DataRequired()])
    confirm = SubmitField('Fiók törlése')
    cancel = SubmitField('Mégse')