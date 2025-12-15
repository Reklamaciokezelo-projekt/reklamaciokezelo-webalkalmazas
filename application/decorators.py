from flask_login import current_user
from functools import wraps
from flask import abort


# ----------------------------------------------------------------------
# Dekorátor, amely ellenőrzi, hogy a bejelentkezett felhasználó rendelkezik-e a szükséges szerepkörrel.
# Ha nem, akkor 403 Forbidden hibát dob.
# ----------------------------------------------------------------------
def roles_required(*roles):
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            if current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator