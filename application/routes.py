from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_user, current_user, login_required, logout_user
from application import app, db, bcrypt
from application.models import User
from application.forms import NewUserForm, LoginForm, UpdateAccountForm, DeleteAccountForm, ChangePasswordForm


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title='Főoldal')


# Regisztráció
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


# Bejelentkezés
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


# Kijelentkezés
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Felhasználói fiók + adatok módosítása
@app.route('/account', methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    form.original_user = current_user

    if form.validate_on_submit():
        if form.cancel.data:
            flash("A módosítás megszakítva.", "secondary")
            return redirect(url_for('account'))

        current_user.username = form.username.data
        db.session.commit()
        flash("A fiók adatai sikeresen frissültek!", 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username

    return render_template('account.html', form=form, title='Felhasználói fiók')


# Jelszó módosítás
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if form.cancel.data:
            flash("A jelszó módosítása megszakítva.", "secondary")
            return redirect(url_for('account'))

        if bcrypt.check_password_hash(current_user.password, form.current_password.data):
            hashed_pw = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password = hashed_pw
            db.session.commit()
            flash('A jelszó sikeresen módosult.', 'success')
            return redirect(url_for('account'))
        else:
            flash('A megadott jelenlegi jelszó hibás.', 'danger')
    return render_template('change_password.html', form=form)


# Felhasználói fiók törlése
@app.route("/delete_account", methods=["GET", "POST"])
@login_required
def delete_account():
    form = DeleteAccountForm()

    if form.validate_on_submit():
        # Ha a felhasználó megszakítja
        if form.cancel.data:
            flash("A fiók törlése megszakítva.", "secondary")
            return redirect(url_for('account'))
        
        # Jelszavas megerősítés
        if bcrypt.check_password_hash(current_user.password, form.password.data):
            user_id = current_user.id
            logout_user()
            user = User.query.get(user_id)
            db.session.delete(user)
            db.session.commit()
            flash("A fiók sikeresen törölve.", "info")
            return redirect(url_for('home'))
        else:
            flash("Hibás jelszó! A fiók nem lett törölve.", "danger")

    return render_template('delete_account.html', form=form)