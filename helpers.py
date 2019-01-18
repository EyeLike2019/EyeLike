import csv
import urllib.request
import datetime
from cs50 import SQL
from passlib.apps import custom_app_context as pwd_context

from flask import redirect, flash, render_template, request, session
from functools import wraps

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")


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

    username = db.execute("SELECT * FROM users WHERE user_id = :user_id", user_id=user_id)[0]["username"]

    return username


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


def random_upload():
    """Select random row from database"""

    random = db.execute("SELECT username, upload, description, score, timestamp, id FROM uploads ORDER BY RANDOM() LIMIT 1")

    if len(random) < 1:
        print("No pictures")
        flash("No pictures available")
        return None
    else:
        date = random[0]["timestamp"]
        date = date[5:16]
        random[0]["timestamp"] = date
        print(random)
        return random

def update_score(change, photo_id):
    """Update post's score"""

    db.execute("UPDATE uploads SET score = score + :change WHERE id=:photo_id", change=change, photo_id=photo_id)
    return

def upload_photo(user_id, upload, description, username):
    """Upload image into database"""

    db.execute("INSERT INTO uploads (user_id, upload, description, username) VALUES(:user_id, :upload, :description, :username)",
               user_id=user_id, upload=upload, description=description, username=username)

    return

def all_photos(user_id):
    """Get all photo's of user"""

    # query database for user's uploads
    user_photos = db.execute("SELECT upload FROM uploads WHERE user_id = :user_id", user_id=user_id)

    return user_photos

def follow_user(user_id, follower_id):
    """Follow user"""

    db.execute("INSERT INTO followers (user_id, follower_id) VALUES(:user_id, :follower_id)",
               user_id=user_id, follower_id=follower_id)
    return

def unfollow_user(user_id, follower_id):
    """Unfollow user"""

    db.execute("DELETE FROM followers WHERE user_id = :user_id AND follower_id = :follower_id", user_id = user_id, follower_id = follower_id)
    return

def is_following(user_id, follower_id):
    follow = db.execute("SELECT follower_id, user_id FROM followers WHERE user_id = :user_id AND follower_id = :follower_id", user_id=user_id, follower_id=follower_id)
    if len(follow) != 1:
        print("Not following")
        return False
    else:
        print("Already following")
        return True

def get_followers(user_id):
    """Get all followers of user"""

    # query database for user's uploads
    followers = db.execute("SELECT follower_id FROM followers WHERE user_id = :user_id", user_id=user_id)

    return followers

def get_following(follower_id):
    """Get all following of user"""

    # query database for user's uploads
    following = db.execute("SELECT user_id FROM followers WHERE follower_id = :follower_id", follower_id=follower_id)

    return following

def get_all_uploads(user_id):
    """Get all uploads of user"""

    # query database for user's uploads
    user_photos = db.execute("SELECT id, user_id, upload, description, timestamp, username, score FROM uploads WHERE user_id = :user_id", user_id=user_id)

    return user_photos