from functools import wraps
from flask import abort
from flask_login import current_user

def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            # --- A felhasználó be van-e jelentkezve és a szerepkör neve benne van-e a listában ---
            if not current_user.is_authenticated or current_user.role.name not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_view
    return wrapper