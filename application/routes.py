from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from application import app, db, bcrypt
from application.models import User, Reklamacio, Department, Customer, Product, DefectType, Status, Role, Position
from application.forms import NewUserForm, LoginForm, UpdateUserForm, DeleteAccountForm, ChangePasswordForm, NewReklamacioForm, UpdateReklamacioForm, DeleteReklamation, ReportFilterForm
from application.utils.auth_role import roles_required
from application.utils.helpers import get_or_create_dynamic, get_dashboard_stats, HONAPOK_TELJES
from sqlalchemy import func
from datetime import date, timedelta, datetime
from flask import send_file
from application.utils.pdf_generator import generate_report_pdf



# ----------------------------------------------------------------------
# FŐOLDAL
# ----------------------------------------------------------------------
@app.route('/home')
@login_required
def home():
    # --- Kiszervezett logika meghívása ---
    count, cost, year_cost, return_count, monthly_data, dept_data = get_dashboard_stats()
    
    # --- Aktuális hónap sorszámának lekérése (1-12) és a listából a megfelelő név kiválasztása ---
    # --- A listák indexelése 0-tól (month - 1) ---
    now = datetime.now()
    current_month_name = HONAPOK_TELJES[now.month - 1]

    current_year = now.year
    
    # --- Változók átadása a sablonnak ---
    return render_template('dashboard.html', 
                         title='Áttekintés',
                         current_month_count=count,
                         current_month_cost=cost,
                         current_year_cost=year_cost,
                         current_return_count=return_count,
                         current_month_name=current_month_name,
                         current_year=current_year)


# ----------------------------------------------------------------------
# STATISZTIKAI API
# ----------------------------------------------------------------------
@app.route('/api/dashboard-stats')
@login_required
def dashboard_stats_api():
    # --- Kiszervezett logika meghívása ---
    count, cost, year_cost, return_count, monthly_data, dept_data = get_dashboard_stats()
    
    # --- Adatok visszaadása JSON formátumban ---
    return jsonify({
        'count': count,
        'cost': cost,
        'year_cost': year_cost,
        'return_count': return_count,
        'monthly_data': monthly_data,
        'dept_data': dept_data
    })


# ----------------------------------------------------------------------
# TÁBLÁZAT API
# ----------------------------------------------------------------------
@app.route('/api/recent-reklamaciok')
@login_required
def api_recent_reklamaciok():
    # --- 5 legfrissebb reklamáció (dátum szerint rendezve) ---
    recent_rekl = Reklamacio.query.order_by(
        Reklamacio.complaint_date.desc(), 
        Reklamacio.id.desc()
    ).limit(5).all()
    
    # --- Lekért adatok JSON-kompatibilis alakítása ---
    data = []
    for r in recent_rekl:
        data.append({
            "id": r.id,
            "date": r.complaint_date.strftime('%Y-%m-%d') if r.complaint_date else '-',
            "customer": r.customer.display_name,
            "product_name": r.product.display_name,
            "product_id": r.product_identifier,
            "defect": r.defect_type.display_name,
            "quantity": r.quantity,
            "status": r.status.name,
            "complaint_number": r.complaint_number,
            "department": r.department.display_name,
            "requires_return": r.requires_return,
            "shipping_date": r.shipping_date.strftime('%Y-%m-%d') if r.shipping_date else '-',
            "cost": r.total_cost or 0,
            "user": f"{r.user.surname} {r.user.forename}"
        })
        
    # --- DataTables kompatibilis JSON válasz ---
    return jsonify({"data": data})

    
# ----------------------------------------------------------------------
# REGISZTRÁCIÓ (Admin)
# – új felhasználó létrehozása 
# ----------------------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def register():
    form = NewUserForm()

    # --- SelecField-ek feltöltése (ID és Név párok) ---
    positions = Position.query.order_by(Position.display_name).all()
    form.position.choices = [(str(p.id), p.display_name) for p in positions]

    # --- Alapértelmezett szerepkör (GET) ---
    if request.method == 'GET':
        default_role = Role.query.filter_by(name='user').first()
        if default_role:
            form.role.data = default_role

    # --- Bejövő form adatok érvényesítése (POST) ---
    if form.validate_on_submit():

        # --- Segédfüggvény használata (helpers.py) ---
        final_position = get_or_create_dynamic(Position, request.form.get('position'))

        # --- Adatok formázása ---
        formatted_surname = form.surname.data.strip().title()
        formatted_forename = form.forename.data.strip().title()

        # --- Jelszó hash-elés (bcrypt) ---
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # --- Új User példány létrehozása ---
        user = User(
            surname=formatted_surname,
            forename=formatted_forename, 
            position=final_position, 
            username=form.username.data, 
            email=form.email.data,
            password=hashed_password, 
            role_id=form.role.data.id
        )
        
        db.session.add(user)
        
        # --- Tranzakció lezárása ---
        try:
            db.session.commit()
            flash(f"{user.surname} {user.forename} felhasználó sikeresen hozzáadva!", "success")
            return redirect(url_for('profiles'))
        except Exception as e:
            db.session.rollback()
            flash("Hiba történt a mentés során! (Adatbázis rollback lefutott)", "danger")
            
    return render_template('register.html', title="Felhasználói fiók létrehozása", form=form)


# ----------------------------------------------------------------------
# GYÖKÉR ÚTVONAL
# – átirányítás a hitelesítési állapot alapján
# ----------------------------------------------------------------------
@app.route('/')
def root():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


# ----------------------------------------------------------------------
# BEJELENTKEZÉS 
# – felhasználó autentikáció (Flask-Login)
# ----------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    # --- Hitelesített felhasználó átirányítása ---
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()

    # --- Bejövő form adatok érvényesítése (POST) ---
    if form.validate_on_submit():
        
        # --- Felhasználó lekérése email alapján ---
        user = User.query.filter_by(email=form.email.data).first()

        # --- Hibakeresés ---
        """ print(f"Beírt email: {form.email.data}")
        print(f"Talált felhasználó: {user}")
        if user:
            is_valid = bcrypt.check_password_hash(user.password, form.password.data)
            print(f"Jelszó egyezik: {is_valid}") """

        # --- Jelszó ellenőrzés és beléptetés ---
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # --- Sikeres autentikáció → felhasználói fiók oldalra ---
            return redirect(url_for('home'))
        else:
            # --- Sikertelen próbálkozás visszajelzése ---
            flash("Sikertelen bejelentkezés. Hibás felhasználónév vagy jelszó", 'danger')
    return render_template('login.html', title='Bejelentkezés', form=form)


# ----------------------------------------------------------------------
# KIJELENTKEZÉS
# ----------------------------------------------------------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


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
# – összes felhasználó megjelenítése (datatables.js)
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

    # --- Bejövő form adatok érvényesítése (POST) ---
    if form.validate_on_submit():

        # --- Jelenlegi jelszó ellenőrzése (biztonsági hitelesítés) ---
        if bcrypt.check_password_hash(current_user.password, form.current_password.data):
            
            # --- Új jelszó hash-elés és mentés ---
            hashed_pw = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password = hashed_pw

            # --- Tranzakció lezárása ---
            db.session.commit()
            flash('A jelszó sikeresen módosult.', 'success')
            return redirect(url_for('account'))
        else:
            # --- Hibaüzenet hibás hitelesítés esetén ---
            flash('A megadott jelenlegi jelszó hibás.', 'danger')

    return render_template('change_password.html', form=form)


# ----------------------------------------------------------------------
# FELHASZNÁLÓ ADATAINAK MODOSÍTÁSA (Admin)
# - Kiolvasás user_id alapján
# ----------------------------------------------------------------------
@app.route("/update_user/<int:user_id>", methods=["GET", "POST"])
@login_required
@roles_required('admin')
def update_user(user_id):

    # --- Felhasználó és űrlap példányosítása ---
    user = User.query.get_or_404(user_id)
    form = UpdateUserForm(original_username=user.username, original_email=user.email)

    # --- Selectfield feltöltése (position) ---
    positions = Position.query.order_by(Position.display_name).all()
    form.position.choices = [(str(p.id), p.display_name) for p in positions]

    # --- Bejövő form adatok érvényesítése (POST) ---
    if form.validate_on_submit():

        # --- Művelet megszakítása ---
        if form.cancel.data:
            flash("A módosítás megszakítva.", "secondary")
            return redirect(url_for('profiles'))

        # --- Segédfüggvény használata (helpers.py) ---
        final_position = get_or_create_dynamic(Position, request.form.get('position'))

        # --- Adatok frissítése az objektumban ---
        user.surname = form.surname.data.strip().title()
        user.forename = form.forename.data.strip().title()
        user.position = final_position
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data

        # --- Tranzakció lezárása ---
        try:
            db.session.commit()
            flash(f"{user.surname} {user.forename} adatai sikeresen frissítve!", "success")
            return redirect(url_for('profiles'))
        except Exception as e:
            db.session.rollback()
            flash("Hiba történt a módosítás során!", "danger")

    # --- Űrlap feltöltése az adatbázis adataival (GET) ---
    elif request.method == 'GET':
        form.surname.data = user.surname
        form.forename.data = user.forename
        form.username.data = user.username
        form.email.data = user.email
        form.role.data = user.role
        
        # --- Aktuális pozíció ID beállítása a kiválasztáshoz ---
        if user.position:
            form.position.data = str(user.position.id)

    return render_template("update_user.html", form=form, user=user)


# ----------------------------------------------------------------------
# FELHASZNÁLÓI FIÓK TÖRLÉSE (Admin)
# - user_id alapján
# - A törlés végleges
# ----------------------------------------------------------------------
@app.route("/delete_account/<int:user_id>", methods=["GET", "POST"])
@login_required
@roles_required('admin')
def delete_account(user_id):
    form = DeleteAccountForm()

    # --- Felhasználó lekérése (ha nem létezik 404) ---
    user = User.query.get_or_404(user_id)

    # --- Bejövő form adatok érvényesítése (POST) ---
    if form.validate_on_submit():
        
        # --- Művelet megszakítása ---
        if form.cancel.data:
            flash("A fiók törlése megszakítva.", "secondary")
            return redirect(url_for('profiles'))
        
        # --- Törlés végrehajtása és mentés ---
        if form.submit.data:
            db.session.delete(user)
            db.session.commit()
            flash("A fiók sikeresen törölve.", "info")
            return redirect(url_for('profiles'))

    return render_template('delete_account.html', form=form, user=user)


# ----------------------------------------------------------------------
# ÚJ REKLAMÁCIÓ
# - új reklamáció felvétele
# - csak super_user
# ----------------------------------------------------------------------
@app.route('/reklamacio/uj', methods=['GET', 'POST'])
@login_required
@roles_required('super_user')
def uj_reklamacio():
    form = NewReklamacioForm()

    # --- SelecField-ek feltöltése (ID és Név párok) ---
    departments = Department.query.order_by(Department.display_name).all()
    form.department.choices = [(str(d.id), d.display_name) for d in departments]

    customers = Customer.query.order_by(Customer.display_name).all()
    form.customer.choices = [(str(c.id), c.display_name) for c in customers]

    products = Product.query.order_by(Product.display_name).all()
    form.product.choices = [(str(p.id), p.display_name) for p in products]

    defect_types = DefectType.query.order_by(DefectType.display_name).all()
    form.defect_type.choices = [(str(d.id), d.display_name) for d in defect_types]

    statuses = Status.query.order_by(Status.display_name).all()
    form.status.choices = [(str(s.id), s.display_name) for s in statuses]

    # --- Bejövő form adatok érvényesítése (POST) ---
    if form.validate_on_submit():
        try:
            # --- Dinamikus mezők feldolgozása (helpers.py) ---
            final_department = get_or_create_dynamic(Department, request.form.get('department'))
            final_customer   = get_or_create_dynamic(Customer, request.form.get('customer'))
            final_product    = get_or_create_dynamic(Product, request.form.get('product'))
            final_defect     = get_or_create_dynamic(DefectType, request.form.get('defect_type'))
            final_status     = get_or_create_dynamic(Status, request.form.get('status'))

            # --- Új Reklamáció példány létrehozása ---
            uj_reklamacio = Reklamacio(
                complaint_date=form.complaint_date.data,
                complaint_number=form.complaint_number.data,
                product_identifier=form.product_identifier.data,
                quantity=form.quantity.data,
                requires_return=form.requires_return.data,
                description=form.description.data,
                shipping_date=form.shipping_date.data,
                total_cost=form.total_cost.data,
                
                # --- Kapcsolatok beállítása (Objektumok átadása) ---
                user=current_user,
                department=final_department,
                customer=final_customer,
                product=final_product,
                defect_type=final_defect,
                status=final_status
            )

            # --- Tranzakció lezárása ---
            db.session.add(uj_reklamacio)
            db.session.commit()
            
            flash(f"A {uj_reklamacio.complaint_number} számú reklamáció sikeresen rögzítve!", "success")
            return redirect(url_for('reklamaciok'))

        except Exception as e:
            # --- Hiba esetén adatbázis rollback ---
            db.session.rollback()
            app.logger.error(f"Hiba a reklamáció mentésekor: {e}")
            flash("Hiba történt az adatbázis mentése során. Kérjük, próbálja újra.", "danger")

    return render_template('reklamacio_uj.html', title='Új Reklamáció Rögzítése', form=form)


# ----------------------------------------------------------------------
# REKLAMÁCIÓK MEGJELENÍTÉSE
# ----------------------------------------------------------------------
@app.route("/reklamaciok")
@login_required
def reklamaciok():
    # --- Összes reklamációt csökkenő dátum szerint ---
    rekl = Reklamacio.query.order_by(Reklamacio.complaint_date.desc()).all()
    return render_template('reklamaciok.html', title='Reklamációk', rekl=rekl)


# ----------------------------------------------------------------------
# REKLAMÁCIÓ MÓDOSÍTÁSA
# - Kiolvasás reklamacio_id alapján
# - csak super_user
# ----------------------------------------------------------------------
@app.route('/reklamacio/modositas/<int:reklamacio_id>', methods=['GET', 'POST'])
@login_required
@roles_required('super_user')
def modosit_reklamacio(reklamacio_id):
    
    # --- Reklamáció lekérése az adatbázisból (vagy 404) ---
    reklamacio = Reklamacio.query.get_or_404(reklamacio_id)
    
    # --- Űrlap példányosítása az eredeti számmal a validáláshoz ---
    form = UpdateReklamacioForm(original_complaint_number=reklamacio.complaint_number)

    # --- SelectField-ek feltöltése (ID és Név párok) ---
    departments = Department.query.order_by(Department.display_name).all()
    form.department.choices = [(str(d.id), d.display_name) for d in departments]

    customers = Customer.query.order_by(Customer.display_name).all()
    form.customer.choices = [(str(c.id), c.display_name) for c in customers]

    products = Product.query.order_by(Product.display_name).all()
    form.product.choices = [(str(p.id), p.display_name) for p in products]

    defect_types = DefectType.query.order_by(DefectType.display_name).all()
    form.defect_type.choices = [(str(d.id), d.display_name) for d in defect_types]

    statuses = Status.query.order_by(Status.display_name).all()
    form.status.choices = [(str(s.id), s.display_name) for s in statuses]

    # --- Bejövő form adatok érvényesítése (POST) ---
    if form.validate_on_submit():

        if form.cancel.data:
            flash("A módosítás megszakítva.", "secondary")
            return redirect(url_for('reklamaciok'))

        # --- Dinamikus mezők feldolgozása a helperrel (helpers.py) ---
        final_department = get_or_create_dynamic(Department, request.form.get('department'))
        final_customer   = get_or_create_dynamic(Customer, request.form.get('customer'))
        final_product    = get_or_create_dynamic(Product, request.form.get('product'))
        final_defect     = get_or_create_dynamic(DefectType, request.form.get('defect_type'))
        final_status     = get_or_create_dynamic(Status, request.form.get('status'))

        # --- Adatok frissítése az objektumban (UPDATE) ---
        reklamacio.complaint_date = form.complaint_date.data
        reklamacio.complaint_number = form.complaint_number.data
        reklamacio.product_identifier = form.product_identifier.data
        reklamacio.quantity = form.quantity.data
        reklamacio.requires_return = form.requires_return.data
        reklamacio.description = form.description.data
        reklamacio.shipping_date = form.shipping_date.data
        reklamacio.total_cost = form.total_cost.data

        # --- Kapcsolatok (objektumok) frissítése ---
        reklamacio.department = final_department
        reklamacio.customer = final_customer
        reklamacio.product = final_product
        reklamacio.defect_type = final_defect
        reklamacio.status = final_status

        # --- Tranzakció lezárása ---
        try:
            db.session.commit()
            flash(f"A {reklamacio.complaint_number} számú reklamáció sikeresen frissítve!", "success")
            return redirect(url_for('reklamaciok'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Hiba a reklamáció módosításakor: {e}")
            flash("Hiba történt a módosítás során! (Adatbázis rollback)", "danger")

    # --- Űrlap feltöltése az adatbázis adataival (GET) ---
    elif request.method == 'GET':
        form.complaint_date.data = reklamacio.complaint_date
        form.complaint_number.data = reklamacio.complaint_number
        form.product_identifier.data = reklamacio.product_identifier
        form.quantity.data = reklamacio.quantity
        form.requires_return.data = reklamacio.requires_return
        form.description.data = reklamacio.description
        form.shipping_date.data = reklamacio.shipping_date
        form.total_cost.data = reklamacio.total_cost
        
        # --- Aktuális dinamikus értékek ID-jának beállítása ---
        if reklamacio.department:
            form.department.data = str(reklamacio.department.id)
        if reklamacio.customer:
            form.customer.data = str(reklamacio.customer.id)
        if reklamacio.product:
            form.product.data = str(reklamacio.product.id)
        if reklamacio.defect_type:
            form.defect_type.data = str(reklamacio.defect_type.id)
        if reklamacio.status:
            form.status.data = str(reklamacio.status.id)

    return render_template("update_rekl.html", form=form, reklamacio=reklamacio)


# ----------------------------------------------------------------------
# REKLAMÁCIÓ TÖRLÉSE
# - csak super_user
# ----------------------------------------------------------------------
@app.route('/reklamacio/torles/<int:reklamacio_id>', methods=['GET', 'POST'])
@login_required
@roles_required('super_user')
def torol_reklamacio(reklamacio_id):

    # --- Reklamáció lekérése az adatbázisból (vagy 404) ---
    reklamacio = Reklamacio.query.get_or_404(reklamacio_id)
    form = DeleteReklamation()

    # --- Törlési szándék megerősítése (POST) ---
    if form.validate_on_submit():

        # --- Rekord eltávolítása és véglegesítés ---
        db.session.delete(reklamacio)
        db.session.commit()
        flash(f"A {reklamacio.complaint_number} reklamáció törlésre került.", "success")
        return redirect(url_for('reklamaciok'))

    return render_template('delete_rekl.html', form=form, reklamacio=reklamacio)


# ----------------------------------------------------------------------
# RIPORTOK ÉS STATISZTIKÁK
# - Csak super_user
# - Chart.js adatok előkészítése (PostgreSQL kompatibilis)
# ----------------------------------------------------------------------
@app.route('/reports', methods=['GET', 'POST'])
@login_required
@roles_required('super_user')
def reports():
    form = ReportFilterForm()

    # --- Alapértelmezett időszak beállítása (utolsó 30 nap) ---
    if request.method == 'GET':
        form.start_date.data = date.today() - timedelta(days=30)
        form.end_date.data = date.today()

    # --- Adatok inicializálása a grafikonhoz ---
    chart_labels = []
    chart_values = []
    chart_type = 'bar'

    # --- Bejövő form adatok érvényesítése (POST) ---
    if form.validate_on_submit():
        start = form.start_date.data
        end = form.end_date.data
        group_criterion = form.group_by.data
        chart_type = form.chart_type.data

        # --- Lekérdezés alapja (inicializálás) ---
        query = None

        # --- Dinamikus lekérdezés összeállítása a kritérium alapján ---

        # --- Hiba típus ---
        if group_criterion == 'defect_type':
            query = db.session.query(DefectType.display_name, func.count(Reklamacio.id))\
                .join(Reklamacio.defect_type)\
                .group_by(DefectType.display_name)
        
        # --- Vevő ---
        elif group_criterion == 'customer':
            query = db.session.query(Customer.display_name, func.count(Reklamacio.id))\
                .join(Reklamacio.customer)\
                .group_by(Customer.display_name)
        
        # --- Termék ---
        elif group_criterion == 'product':
            query = db.session.query(Product.display_name, func.count(Reklamacio.id))\
                .join(Reklamacio.product)\
                .group_by(Product.display_name)

        # --- Státusz ---
        elif group_criterion == 'status':
            query = db.session.query(Status.display_name, func.count(Reklamacio.id))\
                .join(Reklamacio.status)\
                .group_by(Status.display_name)
            
        # --- Üzemegység ---
        elif group_criterion == 'department':
            query = db.session.query(Department.display_name, func.count(Reklamacio.id))\
                .join(Reklamacio.department)\
                .group_by(Department.display_name)

        # --- Havi költség ---
        elif group_criterion == 'monthly_cost':
            month_format = func.to_char(Reklamacio.complaint_date, 'YYYY-MM')
            query = db.session.query(month_format, func.sum(Reklamacio.total_cost))\
                .group_by(month_format)\
                .order_by(month_format)

        # --- Havi darabszám ---   
        elif group_criterion == 'monthly_count':
            month_format = func.to_char(Reklamacio.complaint_date, 'YYYY-MM')
            query = db.session.query(month_format, func.count(Reklamacio.id))\
                .group_by(month_format)\
                .order_by(month_format)

        # --- Lekérdezés futtatása és szűrés ---
        if query:
            results = query.filter(Reklamacio.complaint_date.between(start, end)).all()

            # --- Adatok szétválogatása a Chart.js számára ---
            for row in results:
                # --- row[0]: Kategória név vagy Hónap ---
                # --- row[1]: Darabszám vagy Összeg ---
                chart_labels.append(str(row[0]) if row[0] else "Nincs adat")
                
                # --- Biztonságos típuskonverzió: ha a sum() None-t adna vissza, legyen 0 ---
                val = row[1] if row[1] is not None else 0
                chart_values.append(float(val))

    return render_template('reports.html', 
                           form=form, 
                           labels=chart_labels, 
                           values=chart_values, 
                           chart_type=chart_type)


# ----------------------------------------------------------------------
# RIPORTOK NYOMTATÁSA PDF-BEN
# - Csak super_user
# ----------------------------------------------------------------------
@app.route('/reports/download', methods=['POST'])
@login_required
@roles_required('super_user')
def download_report_pdf():
    # --- Form adatok kinyerése a kérésből ---
    start_str = request.form.get('start_date')
    end_str = request.form.get('end_date')
    group_criterion = request.form.get('group_by')

    # --- Diagram típus és logaritmikus skála kinyerése (alapértelmezett: bar) ---
    chart_type = request.form.get('chart_type', 'bar')
    log_scale_str = request.form.get('log_scale', 'false')
    use_log_scale = (log_scale_str == 'true')

    # --- Dátumok visszaalakítása stringből dátum objektummá ---
    start = datetime.strptime(start_str, '%Y-%m-%d').date() if start_str else date.today()
    end = datetime.strptime(end_str, '%Y-%m-%d').date() if end_str else date.today()

    # --- Lekérdezés újrafuttatása ---
    query = None
    title_suffix = ""

    # --- Hiba típus ---
    if group_criterion == 'defect_type':
        query = db.session.query(DefectType.display_name, func.count(Reklamacio.id))\
            .join(Reklamacio.defect_type).group_by(DefectType.display_name)
        title_suffix = "Hiba típusok szerint"
    
    # --- Vevő ---
    elif group_criterion == 'customer':
        query = db.session.query(Customer.display_name, func.count(Reklamacio.id))\
            .join(Reklamacio.customer).group_by(Customer.display_name)
        title_suffix = "Vevők szerint"

    # --- Termék ---
    elif group_criterion == 'product':
        query = db.session.query(Product.display_name, func.count(Reklamacio.id))\
            .join(Reklamacio.product).group_by(Product.display_name)
        title_suffix = "Termékek szerint"

    # --- Státusz ---
    elif group_criterion == 'status':
        query = db.session.query(Status.display_name, func.count(Reklamacio.id))\
            .join(Reklamacio.status).group_by(Status.display_name)
        title_suffix = "Státusz szerint"

    # --- Üzemegység ---
    elif group_criterion == 'department':
        query = db.session.query(Department.display_name, func.count(Reklamacio.id))\
            .join(Reklamacio.department).group_by(Department.display_name)
        title_suffix = "Üzemegységek szerint"

    # --- Havi költség ---
    elif group_criterion == 'monthly_cost':
        month_format = func.to_char(Reklamacio.complaint_date, 'YYYY-MM')
        query = db.session.query(month_format, func.sum(Reklamacio.total_cost))\
            .group_by(month_format).order_by(month_format)
        title_suffix = "Havi költségbontás"

    # --- Havi darabszám ---
    elif group_criterion == 'monthly_count':
        month_format = func.to_char(Reklamacio.complaint_date, 'YYYY-MM')
        query = db.session.query(month_format, func.count(Reklamacio.id))\
            .group_by(month_format)\
            .order_by(month_format)
        title_suffix = "Havi hibaszám alakulása"

    # --- Adatok kinyerése listákba ---
    labels = []
    values = []
    
    if query:
        results = query.filter(Reklamacio.complaint_date.between(start, end)).all()
        for row in results:
            labels.append(str(row[0]) if row[0] else "Nincs adat")
            val = row[1] if row[1] is not None else 0
            values.append(float(val))

    # --- PDF generálása és küldése ---
    if not labels:
        flash("Nincs adat a PDF generálásához!", "warning")
        return redirect(url_for('reports'))

    # --- paraméterek átadása ---
    pdf_buffer = generate_report_pdf(labels, values, title_suffix, chart_type, use_log_scale)
    
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"riport_{group_criterion}_{date.today()}.pdf",
        mimetype='application/pdf'
    )