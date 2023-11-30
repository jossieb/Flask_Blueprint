"""Helper"""
from functools import wraps
from flask import redirect, render_template, session


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(spec):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            spec = spec.replace(old, new)
        return spec

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(lin):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(lin)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/blue_login")
        return lin(*args, **kwargs)

    return decorated_function
