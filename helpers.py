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


def check_username(username):
    """Check if username exists"""

    usernames = db.execute("SELECT * FROM users WHERE username = :username", username=username)

    return usernames


def check_email(email):
    """Query database for email"""

    emails = db.execute("SELECT * FROM users WHERE email = :email", email=email)

    return emails


def get_username(user_id):
    """Query database for username with user-id"""

    usernames = db.execute("SELECT * FROM users WHERE user_id = :user_id", user_id=user_id)

    return usernames


def get_user_id(username):
    """Query database for user-id"""

    return check_username(username)[0]["user_id"]


def verify_password(username, password):
    """Verify password"""

    # query database for username
    rows = check_username(username)

    return pwd_context.verify(password, rows[0]["hash"])


def register_user(username, password, email):
    """Register user into database"""

    db.execute("INSERT INTO users (username, hash, email) VALUES(:username, :password, :email)",
               username=username, password=pwd_context.hash(password), email=email)

    return


def random_upload(user_id, upload, description, value, timestamp):
    """Select random row from database"""

    random = db.execute("SELECT (username, upload, description, value, timestamp) FROM uploads ORDER BY RAND()")

    return random
