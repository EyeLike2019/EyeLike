import csv
import urllib.request
from cs50 import SQL
from passlib.apps import custom_app_context as pwd_context

from flask import redirect, render_template, request, session
from functools import wraps

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def external_login(username, password):

    # query database for username
    rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

    # ensure username exists and password is correct
    if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
        return -1

    return rows[0]["user_id"]

def external_register(username, email, password):

    # ensure username is not taken
    if len(db.execute("SELECT * FROM users WHERE username=:username", username=username)) > 0:
            return -1

    # stores username, email and hash value of password in database
    db.execute("INSERT INTO users (username, hash, email) VALUES(:username, :password, :email)",
               username=username, password=pwd_context.hash(password), email=email)

    # query database for user-id
    rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

    return rows[0]["user_id"]

def random_upload(user_id, upload, description, value, timestamp):

    # select random row from database
    random = db.execute("SELECT user_id, upload, description, value, timestamp FROM uploads
    ORDER BY RAND()")

    return random
