from functools import wraps
from flask import abort
from flask_login import current_user

def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):

            # --- 1. Autentikáció ellenőrzése (Be van-e jelentkezve?) ---
            if not current_user.is_authenticated:
                abort(401) # 401 Unauthorized
                
            # --- 2. Autorizáció ellenőrzése (Megfelelő a szerepköre?) ---
            if current_user.role.name not in roles:
                abort(403) # 403 Forbidden
                
            return f(*args, **kwargs)
        return decorated_view
    return wrapper