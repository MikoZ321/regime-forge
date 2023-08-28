from flask import redirect, session

def login_required(f):
    """A decorator that forces the user to be logged in"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function