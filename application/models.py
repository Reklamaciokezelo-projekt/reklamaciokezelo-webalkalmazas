from application import db, login_manager
from flask_login import UserMixin
from datetime import date


# --- Flask-Login: betölt egy felhasználót az ID alapján ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ----------------------------------------------------------------------
# USER segédtáblák
# ----------------------------------------------------------------------

# --- Beosztás tábla (Position) ---
class Position(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    display_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Position {self.display_name}>"
    
# --- Szerepkörök tábla (Role) ---
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    display_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Role {self.display_name}>"
    

# ----------------------------------------------------------------------
# USER OSZTÁLY (Felhasználó)
# ----------------------------------------------------------------------
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(50), nullable=False)
    forename = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    # --- Külső kulcsok ---
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id'), nullable=False)

    # --- Kapcsolatok ---
    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    position = db.relationship('Position', backref=db.backref('users', lazy=True))

    @property
    def name(self):
        return f"{self.surname} {self.forename}"
    
    def __repr__(self):
        return f"User ({self.username}, {self.email}, Role: {self.role.name if self.role else 'None'})"
    

# ----------------------------------------------------------------------
# REKLAMÁCIÓ segédtáblák
# ----------------------------------------------------------------------

# --- Üzemegység tábla (Department) ---
class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    display_name = db.Column(db.String(100), nullable=False)

# --- Vevők tábla (Customer) ---
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    display_name = db.Column(db.String(100), nullable=False)

    # --- Display_name nagybetűvé alakítása ---
    def __init__(self, **kwargs):
        super(Customer, self).__init__(**kwargs)
        
        if self.display_name:
            self.display_name = self.display_name.upper()

# --- Termék megnevezés tábla (Product) ---
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    display_name = db.Column(db.String(150), nullable=False)

# --- Hiba megnevezése tábla (DefectType) ---
class DefectType(db.Model):
    __tablename__ = 'defect_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    display_name = db.Column(db.String(150), nullable=False)

# --- Státusz tábla (Status) ---
class Status(db.Model):
    __tablename__ = 'statuses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    display_name = db.Column(db.String(100), nullable=False)



# ----------------------------------------------------------------------
# REKLAMÁCIÓ OSZTÁLY
# ----------------------------------------------------------------------
class Reklamacio(db.Model):
    __tablename__ = 'complaints'

    id = db.Column(db.Integer, primary_key=True)
    complaint_date = db.Column(db.Date, nullable=False)
    complaint_number = db.Column(db.String(50), nullable=False, unique=True)
    product_identifier = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    requires_return = db.Column(db.Boolean, nullable=False, default=False)
    description = db.Column(db.Text, nullable=True)
    shipping_date = db.Column(db.Date, nullable=True)
    total_cost = db.Column(db.Integer, nullable=True, default=0)

    # --- Külső kulcsok (Foreign Keys) ---
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    defect_type_id = db.Column(db.Integer, db.ForeignKey('defect_types.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=False)

    # --- Kapcsolatok (Relationships) ---
    user = db.relationship('User', backref=db.backref('reklamaciok', lazy=True))
    department = db.relationship('Department', backref=db.backref('reklamaciok', lazy=True))
    customer = db.relationship('Customer', backref=db.backref('reklamaciok', lazy=True))
    product = db.relationship('Product', backref=db.backref('reklamaciok', lazy=True))
    defect_type = db.relationship('DefectType', backref=db.backref('reklamaciok', lazy=True))
    status = db.relationship('Status', backref=db.backref('reklamaciok', lazy=True))

    def __repr__(self):
        return f"<Reklamacio {self.complaint_number}>"


