from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import User


# ----------------------------------------------------------------------
# ÚJ FELHASZNÁLÓ LÉTREHOZÁSA ŰRLAP
# ----------------------------------------------------------------------
class NewUserForm(FlaskForm):
    surname = StringField('Vezetéknév', validators=[DataRequired(), Length(min=2,max=50)])
    forename = StringField('Keresztnév', validators=[DataRequired(), Length(min=2,max=50)])
    position = StringField('Beosztás', validators=[DataRequired(), Length(min=2,max=30)])
    username = StringField('Felhasználónév', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('E-mail cím', validators=[DataRequired(), Email(message="A megadott email cím formailag nem megfelelő")])
    password = PasswordField('Jelszó', validators=[DataRequired()])
    confirm_password = PasswordField('Jelszó még egyszer', validators=[DataRequired(), EqualTo('password', message="Nem egyezik a fent megadott jelszóval")])
    role = SelectField('Felhasználói szint', choices=[('user1', 'Alap felhasználó'), ('user2', 'Haladó felhasználó')], default='user1', validators=[DataRequired()])
    submit = SubmitField('Mentés')

    # Felhasználónév validálása, létezik-e már ilyen felhasználónév
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Ez a felhasználónév már foglalt, adjon meg másikat")
        
    # Email validálása, létezik-e már ilyen felhasználónév
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Ez az email cím már foglalt, adjon meg másikat")
        

# ----------------------------------------------------------------------
# BEJELENTKEZÉS ŰRLAP
# ----------------------------------------------------------------------
class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Jelszó', validators=[DataRequired()])
    remember = BooleanField('Bejelentkezve maradok')
    submit = SubmitField('Bejelentkezés')


# ----------------------------------------------------------------------
# FELHASZNÁLÓI ADATOK MÓDOSÍTÁSA ŰRLAP (Admin)
# ----------------------------------------------------------------------
class UpdateUserData(FlaskForm):
    surname = StringField('Vezetéknév', validators=[DataRequired(), Length(min=2,max=50)])
    forename = StringField('Keresztnév', validators=[DataRequired(), Length(min=2,max=50)])
    position = StringField('Beosztás', validators=[DataRequired(), Length(min=2,max=30)])
    username = StringField('Felhasználónév', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('E-mail', validators=[DataRequired(), Length(min=2,max=30)])
    role = SelectField('Felhasználói szint', choices=[('user1', 'Alap felhasználó'), ('user2', 'Haladó felhasználó')], default='user1', validators=[DataRequired()])
    submit = SubmitField('Változtatások mentése')
    cancel = SubmitField('Mégse')

    # Felhasználónév validálása, létezik-e már ilyen felhasználónév
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and user.id != self.original_user.id:
            raise ValidationError("Ez a felhasználónév már foglalt, adjon meg másikat")
        
    # Email validálása, létezik-e már ilyen felhasználónév
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and user.id != self.original_user.id:
            raise ValidationError("Ez az email cím már használatban van.")


# ----------------------------------------------------------------------
# FELHASZNÁLÓI JELSZÓ MÓDOSÍTÁSA ŰRLAP
# ----------------------------------------------------------------------
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Jelenlegi jelszó', validators=[DataRequired()])
    new_password = PasswordField('Új jelszó', validators=[DataRequired()])
    confirm_password = PasswordField('Új jelszó megerősítése', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Mentés')


# ----------------------------------------------------------------------
# FELHASZNÁLÓI FIÓK TÖRLÉSE ŰRLAP (Admin)
# ----------------------------------------------------------------------
class DeleteAccountForm(FlaskForm):
    confirm = SubmitField('Fiók törlése')
    cancel = SubmitField('Mégse')