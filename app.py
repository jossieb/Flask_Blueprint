"""Python Flask Blueprint"""
# Python Flask Blueprint
# By:    Jos van der Have
# Date:  fall 2023
############################################################################################
# Version : 0.1
############################################################################################
# (A) INIT
import sqlite3
from datetime import datetime
import pytz
import logging
from tempfile import mkdtemp
from flask import Flask, render_template, request, make_response, session, redirect, url_for
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import apology, login_required
import local
import locale

# Configure application
app = Flask(__name__)

# (B) SETTINGS

# configure logging level
logging.basicConfig(level=logging.DEBUG)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    """No caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure SQLite database
con = sqlite3.connect(local.db_name, check_same_thread=False)
print("Opened database successfully")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# use right time zone
UTC = pytz.utc
CET = pytz.timezone("Europe/Amsterdam")
datetime_cet = datetime.now(CET)
locale.setlocale(locale.LC_TIME, 'nl_NL.UTF-8')

# (C) ROUTES
############################################################################################


@app.route("/")
def index():
    """main HTML"""

    return render_template("index.html")
############################################################################################

@app.route("/blue_secured")
@login_required
def blue_secured():
    """Secured page"""

    return render_template("secured.html")

############################################################################################

@app.route("/blue_open")
def blue_open():
    """open page"""

    return render_template("open.html")
############################################################################################

@app.route("/blue_login", methods=["GET", "POST"])
def blue_login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Login: u dient eerst in te loggen", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Login: geef een geldig wachtwoord", 400)
        myuser = request.form.get("username")
        myuser = myuser.lower()
        mypass = request.form.get("password")

        # Test the credentials against the local configuration
        if not myuser in ["test", "Test", "TEST"]:
            return apology("Login: user onbekend", 400)
        if mypass != "T3st!":
            return apology("Login: wachtwoord onjuist", 400)
        # Redirect user to home page
        session["user_id"] = myuser
        return render_template("index.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
############################################################################################

def errorhandler(mye):
    """Handle error"""
    if not isinstance(mye, HTTPException):
        mye = InternalServerError()
    return apology(mye.name, mye.code)

############################################################################################

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

############################################################################################