from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, DateField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from application.models import User, Reklamacio, Role, Position
from wtforms_sqlalchemy.fields import QuerySelectField


# ----------------------------------------------------------------------
# ÚJ FELHASZNÁLÓ LÉTREHOZÁSA
# ----------------------------------------------------------------------
class NewUserForm(FlaskForm):
    
    surname = StringField('Vezetéknév', validators=[DataRequired(), Length(min=2,max=50)])
    forename = StringField('Keresztnév', validators=[DataRequired(), Length(min=2,max=50)])
    position = SelectField('Beosztás', validators=[DataRequired()], validate_choice=False)
    username = StringField('Felhasználónév', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('E-mail cím', validators=[DataRequired(), Email(message="A megadott email cím formailag nem megfelelő")])
    password = PasswordField('Jelszó', validators=[DataRequired()])
    confirm_password = PasswordField('Jelszó még egyszer', validators=[DataRequired(), EqualTo('password', message="Nem egyezik a fent megadott jelszóval")])
    
    role = QuerySelectField('Felhasználói szint', 
                            query_factory=lambda: Role.query.all(),
                            get_label='display_name',
                            allow_blank=False)
    
    submit = SubmitField('Mentés')
    cancel = SubmitField('Mégse')

    # --- Egyedi validátor: Felhasználónév ellenőrzése ---
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Ez a felhasználónév már foglalt, adjon meg másikat")
        
    # --- Egyedi validátor: Email cím ellenőrzése ---
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Ez az email cím már foglalt, adjon meg másikat")

        
# ----------------------------------------------------------------------
# BEJELENTKEZÉS
# ----------------------------------------------------------------------
class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Jelszó', validators=[DataRequired()])
    remember = BooleanField('Bejelentkezve maradok')
    submit = SubmitField('Bejelentkezés')


# ----------------------------------------------------------------------
# FELHASZNÁLÓI ADATOK MÓDOSÍTÁSA (Admin)
# ----------------------------------------------------------------------
class UpdateUserForm(FlaskForm):
    surname = StringField('Vezetéknév', validators=[DataRequired(), Length(min=2,max=50)])
    forename = StringField('Keresztnév', validators=[DataRequired(), Length(min=2,max=50)])
    position = SelectField('Beosztás', validators=[DataRequired()], validate_choice=False)
    username = StringField('Felhasználónév', validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('E-mail cím', validators=[DataRequired(), Email(message="A megadott email cím formailag nem megfelelő")])
    
    role = QuerySelectField('Felhasználói szint', 
                            query_factory=lambda: Role.query.all(),
                            get_label='display_name',
                            allow_blank=False)
    
    submit = SubmitField('Mentés')
    cancel = SubmitField('Mégse')

    # --- Konstruktor: eredeti adatok átadása az űrlapnak ---
    def __init__(self, original_username, original_email, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    # --- Egyedi validátor: Felhasználónév (csak változás esetén ellenőriz) ---
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Ez a felhasználónév már foglalt, adjon meg másikat")
            
    # --- Egyedi validátor: Email cím (csak változás esetén ellenőriz) ---
    def validate_email(self, email):  
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Ez az email cím már foglalt, adjon meg másikat")


# ----------------------------------------------------------------------
# FELHASZNÁLÓI JELSZÓ MÓDOSÍTÁSA
# ----------------------------------------------------------------------
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Jelenlegi jelszó', validators=[DataRequired()])
    new_password = PasswordField('Új jelszó', validators=[DataRequired()])
    confirm_password = PasswordField('Új jelszó megerősítése', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Mentés')


# ----------------------------------------------------------------------
# FELHASZNÁLÓI FIÓK TÖRLÉSE (Admin)
# ----------------------------------------------------------------------
class DeleteAccountForm(FlaskForm):
    submit = SubmitField('Fiók törlése')
    cancel = SubmitField('Mégse')


# ----------------------------------------------------------------------
# ÚJ REKLAMÁCIÓ FELVÉTELE
# ----------------------------------------------------------------------
class NewReklamacioForm(FlaskForm):
    
    complaint_date = DateField('Reklamáció dátuma', format='%Y-%m-%d', validators=[DataRequired()])
    complaint_number = StringField('Reklamáció száma', validators=[DataRequired(), Length(min=3, max=50)])
    product_identifier = StringField('Cikkszám / Termék azonosító', validators=[DataRequired()], render_kw={"placeholder": "pl. 15624895"})
    quantity = IntegerField('Reklamált darab (NOK)', validators=[DataRequired(), NumberRange(min=1)])
    requires_return = BooleanField('Visszaszállítást igényel?')
    description = TextAreaField('Hiba rövid leírása', validators=[DataRequired()])
    shipping_date = DateField('Kiszállítás dátuma', format='%Y-%m-%d', validators=[DataRequired()])
    total_cost = IntegerField('Reklamációs költség (HUF)', validators=[NumberRange(min=0)])

    # --- Dinamikus Select mezők (Tom Selecthez) ---
    department = SelectField('Üzemegység', choices=[], validate_choice=False, validators=[DataRequired()])   
    customer = SelectField('Vevő', choices=[], validate_choice=False, validators=[DataRequired()]) 
    product = SelectField('Termék megnevezés', choices=[], validate_choice=False, validators=[DataRequired()])
    defect_type = SelectField('Hiba típusa', choices=[], validate_choice=False, validators=[DataRequired()])
    status = SelectField('Státusz', choices=[], validate_choice=False, validators=[DataRequired()])

    submit = SubmitField('Mentés')
    cancel = SubmitField('Mégse')

    # --- Egyedi validátor: Egyedi reklamációszám ellenőrzése ---
    def validate_complaint_number(self, complaint_number):
        complaint = Reklamacio.query.filter_by(complaint_number=complaint_number.data).first()
        if complaint:
            raise ValidationError("Már létezik ilyen reklamációszám. Kérjük, adjon meg egy egyedit!")
        

# ----------------------------------------------------------------------
# REKLAMÁCIÓ MÓDOSÍTÁSA
# ----------------------------------------------------------------------
class UpdateReklamacioForm(FlaskForm):
    
    complaint_date = DateField('Reklamáció dátuma', format='%Y-%m-%d', validators=[DataRequired()])
    complaint_number = StringField('Reklamáció száma', validators=[DataRequired(), Length(min=3, max=50)])
    product_identifier = StringField('Cikkszám / Termék azonosító', validators=[DataRequired()], render_kw={"placeholder": "pl. 15624895"})
    quantity = IntegerField('Reklamált darab (NOK)', validators=[DataRequired(), NumberRange(min=1)])
    requires_return = BooleanField('Visszaszállítást igényel?')
    description = TextAreaField('Hiba rövid leírása', validators=[DataRequired()])
    shipping_date = DateField('Kiszállítás dátuma', format='%Y-%m-%d', validators=[DataRequired()])
    total_cost = IntegerField('Reklamációs költség (HUF)', validators=[NumberRange(min=0)])

    # --- Dinamikus Select mezők (Tom Selecthez) ---
    department = SelectField('Üzemegység', choices=[], validate_choice=False, validators=[DataRequired()])   
    customer = SelectField('Vevő', choices=[], validate_choice=False, validators=[DataRequired()]) 
    product = SelectField('Termék megnevezés', choices=[], validate_choice=False, validators=[DataRequired()])
    defect_type = SelectField('Hiba típusa', choices=[], validate_choice=False, validators=[DataRequired()])
    status = SelectField('Státusz', choices=[], validate_choice=False, validators=[DataRequired()])

    submit = SubmitField('Mentés')
    cancel = SubmitField('Mégse')

    # --- Konstruktor: eredeti adatok átadása az űrlapnak ---
    def __init__(self, original_complaint_number, *args, **kwargs):
        super(UpdateReklamacioForm, self).__init__(*args, **kwargs)
        self.original_complaint_number = original_complaint_number

    # --- Egyedi validátor:: Csak akkor ellenőriz a DB-ben, ha módosult a szám ---
    def validate_complaint_number(self, complaint_number):
        if complaint_number.data != self.original_complaint_number:
            complaint = Reklamacio.query.filter_by(complaint_number=complaint_number.data).first()
            if complaint:
                raise ValidationError("Már létezik ilyen reklamációszám a rendszerben. Kérjük, adjon meg egy egyedit!")
            

# ----------------------------------------------------------------------
# REKLAMÁCIÓ TÖRLÉSE (Admin)
# ----------------------------------------------------------------------
class DeleteReklamation(FlaskForm):
    submit = SubmitField('Fiók törlése')
    cancel = SubmitField('Mégse')


# ----------------------------------------------------------------------
# RIPORT SZŰRŐ
# - Statisztikák lekérdezéséhez
# ----------------------------------------------------------------------
class ReportFilterForm(FlaskForm):
    start_date = DateField('Kezdő dátum', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Záró dátum', format='%Y-%m-%d', validators=[DataRequired()])
    
    # --- Adatok csoportosítása ---
    group_by = SelectField('Csoportosítás szempontja', choices=[
        ('defect_type', 'Hiba típusa szerint'),
        ('customer', 'Vevő szerint'),
        ('product', 'Termék szerint'),
        ('status', 'Státusz szerint'),
        ('department', 'Üzemegység szerint'),
        ('monthly_cost', 'Össz. költség havi bontásban'),
        ('monthly_count', 'Össz. hiba havi bontásban')
    ], validators=[DataRequired()])

    # --- Diagram típus ---
    chart_type = SelectField('Diagram típusa', choices=[
        ('bar', 'Oszlopdiagram'),
        ('line', 'Vonaldiagram'),
        ('pie', 'Kördiagram')
    ], validators=[DataRequired()])

    submit = SubmitField('Riport generálása')
        