import csv
import urllib.request
import random
import requests
import json
import os
from cs50 import SQL
from passlib.apps import custom_app_context as pwd_context

from flask import redirect, flash, render_template, request, session
from functools import wraps

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# declare client-id's API
client_id = ["8f5cd8cd9e1c27d5b5c6d283c243726afcf1a7ad7602c1ee0f6a0702f5272a0f",
             "2a8d0cb26d41c89b6500699b0f67a3d26dda08dead3c5743dae7afec9b9ada21",
             "0efa5a111f97fe99a9dc9fdd81c66b455e0cbb8e7fadbcc1d2a75f1bf501ecb1"]


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

    return "Success"


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
        return random


def update_score(change, photo_id):
    """Update post's score"""

    db.execute("UPDATE uploads SET score = score + :change WHERE id=:photo_id", change=change, photo_id=photo_id)

    return "Success"


def upload_photo(user_id, upload, description, username):
    """Upload image into database"""

    db.execute("INSERT INTO uploads (user_id, upload, description, username) VALUES(:user_id, :upload, :description, :username)",
               user_id=user_id, upload=upload, description=description, username=username)

    return "Success"


def remove_photo(user_id, photo_id):
    """Remove photo from user"""

    db.execute("DELETE FROM uploads WHERE user_id = :user_id AND id = :photo_id",
               user_id=user_id, photo_id=photo_id)

    return "Success"


def follow_user(user_id, follower_id):
    """Follow user"""

    db.execute("INSERT INTO followers (user_id, follower_id) VALUES(:user_id, :follower_id)",
               user_id=user_id, follower_id=follower_id)

    return "Success"


def unfollow_user(user_id, follower_id):
    """Unfollow user"""

    db.execute("DELETE FROM followers WHERE user_id = :user_id AND follower_id = :follower_id",
               user_id=user_id, follower_id=follower_id)

    return "Success"


def is_following(user_id, follower_id):
    """Check if user is following other user"""

    follow = db.execute("SELECT * FROM followers WHERE user_id = :user_id AND follower_id = :follower_id",
                        user_id=user_id, follower_id=follower_id)

    if len(follow) != 1:
        return False
    else:
        return True


def get_followers(user_id):
    """Get all followers of user"""

    followers = db.execute("SELECT follower_id FROM followers WHERE user_id = :user_id", user_id=user_id)

    return followers


def get_following(follower_id):
    """Get all following of user"""

    following = db.execute("SELECT user_id FROM followers WHERE follower_id = :follower_id", follower_id=follower_id)

    return following


def get_all_uploads(user_id):
    """Get all uploads of user"""

    user_photos = db.execute("SELECT * FROM uploads WHERE user_id = :user_id", user_id=user_id)

    # change timestamp to prevered format
    for p in user_photos:
        date = p["timestamp"]
        date = date[5:16]
        p["timestamp"] = date

    return user_photos


def get_all_recents():
    """Get all the photo's posted in the past week"""

    all_recents = db.execute("SELECT * FROM uploads WHERE DATE(timestamp) >= DATE('now', 'weekday 0', '-12 days')")
    for p in all_recents:
        date = p["timestamp"]
        date = date[5:16]
        p["timestamp"] = date
    print(all_recents)

    return all_recents


def get_favourites(user_id):
    """Get all favourites of user"""

    photo_id = db.execute("SELECT photo_id FROM favourites WHERE user_id = :user_id", user_id=user_id)

    return photo_id


def add_favourite(user_id, photo_id):
    """Add favourite into database"""

    db.execute("INSERT INTO favourites (user_id, photo_id) VALUES(:user_id, :photo_id)", user_id=user_id, photo_id=photo_id)

    return "Success"


def remove_favourite(user_id, photo_id):
    """Remove favourite from database"""

    db.execute("DELETE FROM favourites WHERE user_id = :user_id AND photo_id = :photo_id",
               user_id=user_id, photo_id=photo_id)

    return "Success"


def get_info(post_id):
    """Get all info of a post"""

    post_info = db.execute("SELECT * FROM uploads WHERE id=:post_id",
                           post_id=post_id)[0]

    date = post_info["timestamp"]
    date = date[5:16]
    post_info["timestamp"] = date

    return post_info


def update_profile_pic(user_id, file):
    """Updates user's profile picture in database"""

    # check if user already has profile picture
    existing_pic = db.execute("SELECT * FROM profilepictures WHERE user_id=:user_id", user_id=user_id)

    if len(existing_pic) > 0:
        db.execute("UPDATE profilepictures SET profile_picture=:file WHERE user_id=:user_id", file=file, user_id=user_id)

    else:
        db.execute("INSERT INTO profilepictures (user_id, profile_picture) VALUES(:user_id, :file)", user_id=user_id, file=file)

    return "Success"

def remove_profile_pic(user_id):
    """Deletes profile picture of user in database"""

    db.execute("DELETE FROM profilepictures WHERE user_id=:user_id", user_id=user_id)

    return "Success"


def get_profile_pic(user_id):
    """Get profile picture from user"""

    profile_pic = db.execute("SELECT * FROM profilepictures WHERE user_id=:user_id", user_id=user_id)

    return profile_pic


def check_profile_picture(user_id):
    """Check if user has profile picture and return picture"""

    # declare variable
    has_pp = False

    # get user's profile picture
    profile_pic = get_profile_pic(user_id)

    if len(profile_pic) > 0:
        profile_pic = profile_pic[0]["profile_picture"]
        has_pp = True

    else:
        # select random client-id
        id = random.choice(client_id)

        try:
            # get random photo from API
            api = requests.get(
                "https://api.unsplash.com/photos/random?order_by=popular&orientation=squarish&client_id=" + id + "&query=profile-pic&count=30")
            url = json.loads(api.content)
            profile_pic = url[random.randint(1,30)]["urls"]["full"]

        except Exception:
            # if API's request limit is reached, show standard profile picture
            profile_pic = "https://source.unsplash.com/random"

    return profile_pic, has_pp