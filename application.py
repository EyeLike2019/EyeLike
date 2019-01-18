from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_from_directory
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import datetime
import os
import requests
import json
import pprint as pp

from helpers import *

# configure application
app = Flask(__name__)

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(debug=True, host='0.0.0.0')

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# declare upload-folder
UPLOAD_FOLDER = os.path.basename('upload')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
    random2 = random_upload()

    if random2 == None:
        print("No pictures")
        return redirect(url_for("account"))
    else:
        random = random_upload()[0]
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], random["upload"])

        return render_template("index.html", random=random, file=full_filename, photo_id=random["id"])

@app.route("/timeline")
@login_required
def timeline():

    uploads = []
    followings_id = get_following(session["user_id"])

    for p in followings_id:
        user_uploads = get_all_uploads(p["user_id"])
        for u in user_uploads:
            uploads.append(u)
    uploads.sort(key=lambda d: d['timestamp'])

    return render_template("timeline.html", uploads=uploads)


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload_file():
    """Upload a file"""
    if request.method == "POST":
        try:
            # save the file in upload-folder
            file = request.files['file']
            filename = str(session["user_id"]) + "_" + file.filename
            if not filename.endswith(".jpg") and not filename.endswith(".png") and not filename.endswith(".jpeg"):
                flash('Invalid file!')
                return redirect(url_for("index"))


            f = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(f)
            if os.path.getsize(f) > 4194304:
                flash("file size is to big, limit is 4mb")
                os.remove(f)
                return redirect(url_for("index"))
            # upload image into database
            upload_photo(session["user_id"], filename, "test", get_username(session["user_id"]))

            flash('Upload successful')
            return redirect(url_for("index"))
        except Exception:
            flash("Please select photo you want to upload first!")
            return redirect(url_for("index"))

    else:
        # configure API
        api = requests.get("https://api.unsplash.com/photos/random?order_by=popular&orientation=squarish&client_id=2a8d0cb26d41c89b6500699b0f67a3d26dda08dead3c5743dae7afec9b9ada21&query=clothes&count=30")
        url = json.loads(api.content)

        return render_template("upload.html", url=url, url2="&fit=fill&fill=blur&w=250&h=200&dpi=2")

@app.route("/updatescore")
def update():
    """"Update score of upload"""

    change = request.args['newscore']
    photo_id = request.args['photo_id']

    update_score(change, photo_id)
    return "Succes"


@app.route("/account")
@login_required
def account():
    """Show account"""

    # get username
    username = get_username(session["user_id"])

    photos = []
    followers = []
    following = []
    user_photos = all_photos(session["user_id"])
    followers_id = get_followers(session["user_id"])
    followings_id = get_following(session["user_id"])

    # get all followers of user
    for f in followers_id:
        name = get_username(f["follower_id"])
        followers.append(name)

    # get all people whom the user follows
    for j in followings_id:
        name = get_username(j["user_id"])
        following.append(name)

    for p in user_photos:
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], p["upload"])
        photos.append(full_filename)

    return render_template("account.html", name=username, photos=photos, followers=followers, following=following)

@app.route("/profile/<username>")
@login_required
def profile(username):

    # check if username exists
    if len(check_username(username)) != 1:
        flash("Username doesn't exist")
        return redirect(url_for("index"))

    # redirect to account page when searching for self
    if username == get_username(session["user_id"]):
        return redirect(url_for("account"))

    name = username
    photos = []
    followers = []
    following = []
    uid = get_user_id(username)
    follower_id = session["user_id"]
    user_photos = all_photos(uid)
    followers_id = get_followers(uid)
    followings_id = get_following(uid)

    # get all pictures of user
    for p in user_photos:
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], p["upload"])
        photos.append(full_filename)

    # get all followers of user
    for f in followers_id:
        username = get_username(f["follower_id"])
        followers.append(username)

    # get all people whom the user follows
    for j in followings_id:
        name2 = get_username(j["user_id"])
        following.append(name2)


    print(photos, uid, user_photos, followers)
    return render_template("profile.html", name=name, photos=photos, user_id=uid, follower_id=follower_id, followers=followers, following=following)


@app.route("/search/<username>", methods=["GET", "POST"])
def search(username):
    """Search for user"""

    # check if username exists
    if len(check_username(username)) != 1:
        flash("Username doesn't exist")
        return redirect(url_for("index"))

    # redirect to account page when searching for self
    if username == get_username(session["user_id"]):
        return redirect(url_for("account"))

    return redirect(url_for("profile", username=username))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username!")
            return render_template("login.html")

        # ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password!")
            return render_template("login.html")

        # ensure username exists and password is correct
        elif len(check_username(request.form.get("username"))) != 1 or not verify_password(request.form.get("username"), request.form.get("password")):
            flash("Invalid username/password!")
            return render_template("login.html")

        # remember which user has logged in
        session["user_id"] = get_user_id(request.form.get("username"))

        # redirect user to home page
        return redirect(url_for("account"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username!")
            return render_template("register.html")

        # ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password!")
            return render_template("register.html")

        # ensure email was submitted
        elif not request.form.get("email"):
            flash("Must provide email!")
            return render_template("register.html")

        # ensure password was submitted again
        elif not request.form.get("confirmation"):
            flash("Must confirm password!")
            return render_template("register.html")

        # ensure username is not taken
        elif len(check_username(request.form.get("username"))) > 0:
            flash("Username already taken!")
            return render_template("register.html")

        # ensure email is not taken
        elif len(check_email(request.form.get("email"))) > 0:
            flash("Email already taken!")
            return render_template("register.html")

        # ensure password matches with password copy
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords don't match!")
            return render_template("register.html")

        # register user into database
        register_user(request.form.get("username"), request.form.get("password"), request.form.get("email"))

        # remember which user has logged in
        session["user_id"] = get_user_id(request.form.get("username"))

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route('/upload/<path:path>')
def show(path):
    """Show image"""
    return send_from_directory('upload', path)

@app.route("/follow")
def follow():
    """"Follow user"""

    user_id = request.args['user_id']
    follower_id = request.args['follower_id']

    follow_user(user_id, follower_id)
    return "Succes"

@app.route("/already_following")
def already_following():
    """"Check if user already follows"""

    user_id = request.args['user_id']
    follower_id = request.args['follower_id']

    return(str(is_following(user_id, follower_id)))

@app.route("/unfollow")
def unfollow():
    """"Unfollow user"""

    user_id = request.args['user_id']
    follower_id = request.args['follower_id']

    unfollow_user(user_id, follower_id)
    return "Succes"