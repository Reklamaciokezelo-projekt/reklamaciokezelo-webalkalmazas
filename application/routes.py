from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, login_required, logout_user
from application import app, db, bcrypt
from application.models import User
from application.forms import NewUserForm, LoginForm, UpdateUserData, DeleteAccountForm, ChangePasswordForm
from application.decorators import roles_required


# ----------------------------------------------------------------------
# FŐOLDAL
# ----------------------------------------------------------------------
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title='Főoldal')


# ----------------------------------------------------------------------
# REGISZTRÁCIÓ (admin)
# – új felhasználó létrehozása 
# ----------------------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def register():
    form = NewUserForm()

    # POST esetén a bejövő form adatok érvényesítése (WTForms)
    if form.validate_on_submit():

        # A jelszó bcrypt-tel történő hash-elése
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Új User példány létrehozása
        user = User(surname=form.surname.data,
                    forename=form.forename.data, 
                    position=form.position.data,
                    username=form.username.data, 
                    email=form.email.data,
                    password=hashed_password, 
                    role=form.role.data)
        
        # Adatbázis műveletek (INSERT)
        db.session.add(user)
        db.session.commit()
        flash("A fiók elkészült, Jelentkezz be")
        return redirect(url_for('home'))
    return render_template('register.html', title="Felhasználói fiók létrehozása", form=form)


# ----------------------------------------------------------------------
# BEJELENTKEZÉS 
# – felhasználó autentikáció (Flask-Login)
# ----------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    # Ha már hitelesített user érkezik, ne engedje újra a login oldalt.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()

    if form.validate_on_submit():
        # Felhasználó lekérése email alapján
        user = User.query.filter_by(email=form.email.data).first()

        # Jelszó ellenőrzés bcrypt-tel
        if user and bcrypt.check_password_hash(user.password, form.password.data): # beírt jelszó és tárolt jelszó összehasonlítása
            login_user(user, remember=form.remember.data)
            # Sikeres autentikáció → felhasználói fiók oldalra
            return redirect(url_for('account'))
        else:
            flash("Sikertelen bejelentkezés. Hibás felhasználónév vagy jelszó", 'danger')
    return render_template('login.html', title='Bejelentkezés', form=form)


# ----------------------------------------------------------------------
# KIJELENTKEZÉS
# ----------------------------------------------------------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# ----------------------------------------------------------------------
# FELHASZNÁLÓI FIÓK 
# – saját profilnézet (autentikációhoz kötött)
# ----------------------------------------------------------------------
@app.route('/account', methods=["GET", "POST"])
@login_required
def account():
        return render_template('account.html', title='Felhasználói fiók')


# ----------------------------------------------------------------------
# FELHASZNÁLÓK KEZELÉSE (Admin) 
# – összes felhasználó megjelenítése
# ----------------------------------------------------------------------
@app.route("/users")
@login_required
@roles_required('admin')
def profiles():
    users = User.query.all()
    return render_template('users.html', title='Felhasználók', users=users)


# ----------------------------------------------------------------------
# JELSZÓ MÓDOSÍTÁS 
# – jelenlegi jelszó kötelező hitelesítése (bcrypt check)
# ----------------------------------------------------------------------
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():

        # Jelenlegi jelszó validálása
        if bcrypt.check_password_hash(current_user.password, form.current_password.data):
            # Új jelszó generálása és mentése
            hashed_pw = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password = hashed_pw
            db.session.commit()
            flash('A jelszó sikeresen módosult.', 'success')
            return redirect(url_for('account'))
        else:
            flash('A megadott jelenlegi jelszó hibás.', 'danger')

    return render_template('change_password.html', form=form)


# ----------------------------------------------------------------------
# FELHASZNÁLÓ ADATAINAK MODOSÍTÁSA (Admin funkció)
# - Kiolvasás user_id alapján
# ----------------------------------------------------------------------
@app.route("/update_user/<int:user_id>", methods=["GET", "POST"])
@login_required
@roles_required('admin')
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UpdateUserData()

    # Az eredeti user elmentése a form validáláshoz
    form.original_user = user

    if form.validate_on_submit():

        # Megszakítás esetén vissza a listára
        if form.cancel.data:
            flash("A módosítás megszakítva.", "secondary")
            return redirect(url_for('profiles'))

        # Adatok frissítése (UPDATE)
        user.surname = form.surname.data
        user.forename = form.forename.data
        user.position = form.position.data
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data

        db.session.commit()
        flash("A felhasználó adatai frissítve!", "success")
        return redirect(url_for('profiles'))

    # GET kérés → form mezők feltöltése meglévő adatokkal
    form.surname.data = user.surname
    form.forename.data = user.forename
    form.position.data = user.position
    form.username.data = user.username
    form.email.data = user.email
    form.role.data = user.role

    return render_template("update_user.html", form=form, user=user)


# ----------------------------------------------------------------------
# FELHASZNÁLÓI FIÓK TÖRLÉSE
# - user_id alapján
# - Two-step confirmation (WTForms)
# - A törlés végleges
# ----------------------------------------------------------------------
@app.route("/delete_account/<int:user_id>", methods=["GET", "POST"])
@login_required
@roles_required('admin')
def delete_account(user_id):
    form = DeleteAccountForm()

    # Ha a user nem létezik: 404
    user = User.query.get_or_404(user_id)

    if form.validate_on_submit():
        
        # Művelet megszakítása
        if form.cancel.data:
            flash("A fiók törlése megszakítva.", "secondary")
            return redirect(url_for('profiles'))
        
        # Törlés (DELETE FROM users WHERE id = ...)
        if form.confirm.data:
            db.session.delete(user)
            db.session.commit()
            flash("A fiók sikeresen törölve.", "info")
            return redirect(url_for('profiles'))

    return render_template('delete_account.html', form=form, user=user)