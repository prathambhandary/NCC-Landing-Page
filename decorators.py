from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def admin_required(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):

        verify_jwt_in_request(locations=["cookies"])

        identity = get_jwt_identity()

        if identity != "admin":
            return {"error": "Unauthorized"}, 403

        return fn(*args, **kwargs)

    return wrapper