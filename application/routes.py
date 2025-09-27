from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_user, current_user, login_required, logout_user
from application import app, db, bcrypt
from application.models import User
from application.forms import NewUserForm, LoginForm


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title='Főoldal')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = NewUserForm() # forms.py-ból meghívom az osztálykonstruktort
    if form.validate_on_submit(): # ha POST metódussal érkezünk
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("A fiók elkészült, Jelentkezz be")
        print(user.query.all()) # csak ellenőrzésre, kiírja a létrehozott usereket
        return redirect(url_for('home'))
    return render_template('register.html', title="Felhasználói fiók létrehozása", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # ha a felhasználó be van jelentkezve és a login url-re navigál, a rendszer átirányítja a home-ra
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # a megadott adat alapján kiolvasás az adatbázisból
        if user and bcrypt.check_password_hash(user.password, form.password.data): # beírt jelszó és tárolt jelszó összehasonlítása
            login_user(user, remember=form.remember.data)
            return redirect(url_for('account'))
        else:
            flash("Sikertelen bejelentkezés. Hibás felhasználónév vagy jelszó", 'danger')
    return render_template('login.html', title='Bejelentkezés', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Felhasználói fiók')