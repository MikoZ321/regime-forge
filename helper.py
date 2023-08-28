from flask import session


def logged_in():
    if session.get("user_id") == None:
        return True
    return False