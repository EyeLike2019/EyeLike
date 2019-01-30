from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_from_directory
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import datetime
import os

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

# declare profile-folder
PROFILE_FOLDER = os.path.basename('uploadprofilepic')
app.config['PROFILE_FOLDER'] = PROFILE_FOLDER


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

        elif request.form.get("username")[0] != "@":
            username = "@" + request.form.get("username")

        # ensure username exists and password is correct
        if len(check_username(username)) != 1 or not verify_password(username, request.form.get("password")):
            flash("Invalid username/password!")
            return render_template("login.html")

        # remember which user has logged in
        session["user_id"] = get_user_id(username)

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

    # forget all counters
    global counter
    counter = 3

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

        elif request.form.get("username")[0] == "@":
            flash("Username can't begin with this symbol!")
            return render_template("register.html")

        # ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password!")
            return render_template("register.html")

        elif not any(x.isupper() for x in request.form.get("password")) or not any(x.isdigit() for x in request.form.get("password")):
            flash("Password must contain at least one upperchase letter and one digit!")
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
        register_user("@" + request.form.get("username"), request.form.get("password"), request.form.get("email"))

        # remember which user has logged in
        session["user_id"] = get_user_id("@" + request.form.get("username"))

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/account")
@login_required
def account():
    """Show account"""

    photos_empty = False

    # get username
    username = get_username(session["user_id"])

    # declare variables
    followers = []
    following = []
    user_photos = get_all_uploads(session["user_id"])
    followers_id = get_followers(session["user_id"])
    followings_id = get_following(session["user_id"])

    if not user_photos:
        photos_empty = True

    # get all followers of user
    for f in followers_id:
        name = get_username(f["follower_id"])
        followers.append(name)

    # get all people whom the user follows
    for j in followings_id:
        name = get_username(j["user_id"])
        following.append(name)

    # check if user has profile picture and get (random) profile picture
    pp_check = check_profile_picture(get_user_id(username))

    if pp_check[1] == True:
        profile_pic = os.path.join(app.config['PROFILE_FOLDER'], pp_check[0])

    else:
        profile_pic = pp_check[0]

    return render_template("account.html", name=username, photos=user_photos, followers=followers, following=following, profile_pic=profile_pic, has_pp=pp_check[1], num_followers=len(followers), num_following=len(following), photos_empty=photos_empty)


@app.route("/profile/<username>")
@login_required
def profile(username):
    """Show profile of other user"""

    photos_empty = False

    # check if username exists
    if len(check_username(username)) != 1:
        flash("Username doesn't exist")
        return redirect(url_for("index"))

    # redirect to account page when searching for self
    if username == get_username(session["user_id"]):
        return redirect(url_for("account"))

    # declare variables
    followers = []
    following = []
    uid = get_user_id(username)
    follower_id = session["user_id"]
    user_photos = get_all_uploads(uid)
    followers_id = get_followers(uid)
    followings_id = get_following(uid)

    if not user_photos:
        photos_empty = True

    # get all followers of user
    for f in followers_id:
        name = get_username(f["follower_id"])
        followers.append(name)

    # get all people whom the user follows
    for j in followings_id:
        name2 = get_username(j["user_id"])
        following.append(name2)

    # check if user has profile picture and get (random) profile picture
    pp_check = check_profile_picture(get_user_id(username))

    if pp_check[1] == True:
        profile_pic = os.path.join(app.config['PROFILE_FOLDER'], pp_check[0])

    else:
        profile_pic = pp_check[0]

    return render_template("profile.html", name=username, photos=user_photos, user_id=uid, follower_id=follower_id, followers=followers, following=following, profile_pic=profile_pic, has_pp=pp_check[1], num_followers=len(followers), num_following=len(following), photos_empty=photos_empty)


@app.route("/")
def index():
    """Show homepage/random page"""

    # declare variables
    user_id = check_logged_in()
    random_photo = random_upload()
    seen = request_seen(user_id)

    if user_id == 0:
        flash("Log in or register to like and dislike the pictures!")
        return render_template("index.html", random=random_photo[0], user_id=user_id)

    else:
        for post in random_photo:
            if post["id"] not in seen and get_user_id(post["username"]) != user_id:
                return render_template("index.html", random=post, user_id=user_id)

        flash("No more pictures available at the moment! Please come back later!")
        return redirect(url_for("account"))


@app.route("/timeline")
@login_required
def timeline():
    """Show timeline of following accounts"""

    uploads = []
    followings_id = get_following(session["user_id"])

    # get all uploads of following accounts
    for p in followings_id:
        user_uploads = get_all_uploads(p["user_id"])
        for u in user_uploads:
            uploads.append(u)

    # sort uploads on timestamp
    uploads.sort(key=lambda d: d['timestamp'])

    return render_template("timeline.html", uploads=uploads, user_id=session["user_id"])

counter = 3
@app.route("/load_more")
def load_more():
    global counter
    counter += 3

    return str(counter)


@login_required
@app.route("/trending")
def trending():
    """Show trending pictures"""

    trendingphotos = []
    all_recents = get_all_recents()

    # check if the score of the photo is high enough
    for p in all_recents:
        if p["score"] >= 100:
            trendingphotos.append(p)

    # sort uploads on timestamp
    trendingphotos.sort(key=lambda d: d['score'], reverse=True)

    if len(trendingphotos) == 0:
        flash("There aren't any trending pictures!")
        return render_template("trending.html")
    trendingphotos = trendingphotos[:int(counter)]
    return render_template("trending.html", trendingphotos=trendingphotos, user_id=session["user_id"])


@app.route("/favourites")
@login_required
def favourites():
    """Show favourites of user"""

    favourites = []
    post_id = get_favourites(session["user_id"])

    if len(post_id) == 0:
        flash("You have no favourite posts!")
        return render_template("favourites.html")

    # get all uploads of following accounts
    for p in post_id:
        favourites.append(get_info(p["photo_id"]))

    # sort uploads with most recent added upload first
    favourites.reverse()

    return render_template("favourites.html", favourites=favourites, user_id=session["user_id"])


@app.route("/search/<username>", methods=["GET", "POST"])
def search(username):
    """Search for user"""

    # check if @ need to be added
    if username[0] != "@":
        username = "@" + username

    # check if username exists
    if len(check_username(username)) != 1:
        flash("Username doesn't exist")
        return redirect(url_for("index"))

    # redirect to account page when searching for self
    if username == get_username(session["user_id"]):
        return redirect(url_for("account"))

    return redirect(url_for("profile", username=username))


@app.route("/already_following")
def already_following():
    """"Check if user already follows"""

    user_id = request.args['user_id']
    follower_id = request.args['follower_id']

    return(str(is_following(user_id, follower_id)))


@app.route("/follow")
def follow():
    """"Follow user"""

    user_id = request.args['user_id']
    follower_id = request.args['follower_id']

    follow_user(user_id, follower_id)
    return "Succes"


@app.route("/unfollow")
def unfollow():
    """"Unfollow user"""

    user_id = request.args['user_id']
    follower_id = request.args['follower_id']

    unfollow_user(user_id, follower_id)

    return "Succes"


@app.route("/remove")
def remove():
    """"Remove photo"""

    user_id = request.args['user_id']
    photo_id = request.args['photo_id']

    # remove photo from upload folder
    filename = os.path.join(app.config['UPLOAD_FOLDER'], get_info(photo_id)["upload"])
    print(filename)
    # os.remove(filename)

    # remove photo from database
    remove_photo(user_id, photo_id)

    return "Success"


@app.route("/py_autocomplete")
def py_autocomplete():
    """Get all users"""

    users = get_all_users()

    return users


@app.route("/removeprofilepicture")
def rm_profile_picture():
    """Remove profile picture of user"""

    # remove profile picture from upload folder
    filename = request.args["profile_pic"]
    os.remove(filename)

    # remove profile picture from database
    remove_profile_pic(session["user_id"])

    flash("Profile picture deleted!")

    return "Success"


@app.route("/removefavourite")
def rm_favourite():
    """"Remove photo from favourites"""

    user_id = request.args['user_id']
    photo_id = request.args['photo_id']

    remove_favourite(user_id, photo_id)

    return redirect(url_for("favourites"))



@app.route("/addfavourite")
@login_required
def new_favourite():
    """"Add photo to favourites"""

    user_id = int(request.args['user_id'])
    photo_id = int(request.args['photo_id'])

    for post in get_favourites(user_id):
        if post["photo_id"] == photo_id:
            return "NoSucces"

    add_favourite(user_id, photo_id)
    return "Succes"

@app.route("/updatescore")
def update():
    """"Update score of upload"""

    change = request.args['newscore']
    photo_id = request.args['photo_id']

    # update score in database
    update_score(change, photo_id)

    # check if user is logged in and get user_id
    user_id = check_logged_in()

    # keep track of which photo user has seen
    if user_id != 0:
        already_seen(user_id, photo_id)

    return "Succes"


@app.route('/upload/<path:path>')
def show(path):
    """Show image"""

    return send_from_directory('upload', path)


@app.route('/uploadprofilepic/<path:path>')
def show_profile(path):
    """Show image"""

    return send_from_directory('uploadprofilepic', path)


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload_file():
    """Upload a file"""

    if request.method == "POST":

        # save the file in upload-folder
        file = request.files['file']
        filename = str(session["user_id"]) + "_" + file.filename

        # change file type to lowercase
        filename = filename[:-3] + filename[-3:].lower()

        if not filename.endswith(".jpg") and not filename.endswith(".png") and not filename.endswith(".jpeg"):
            flash('Invalid file!')
            return redirect(url_for("account"))

        f = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(f)

        # compress image size via API
        compress_image(f)

        # check if file isn't to big
        if os.path.getsize(f) > 4194304:
            flash("file size is to big, limit is 4mb")
            os.remove(f)
            return redirect(url_for("account"))

        # get description
        description = request.form.get("description")

        # upload image into database
        upload_photo(session["user_id"], filename, description, get_username(session["user_id"]))
        flash('Upload successful')

        return redirect(url_for("account"))

    else:
        return render_template("account.html")


@app.route("/uploadprofilepic", methods=['POST'])
def profile_picture():
    """Update user's profile picture"""

    # save the file in profile-folder
    file = request.files['pf']
    filename = str(session["user_id"]) + "_" + file.filename
    if not filename.endswith(".jpg") and not filename.endswith(".png") and not filename.endswith(".jpeg"):
        flash('Invalid file!')
        return redirect(url_for("account"))

    f = os.path.join(app.config['PROFILE_FOLDER'], filename)

    file.save(f)

    # compress image via API
    compress_image(f)

    if os.path.getsize(f) > 4194304:
        flash("file size is to big, limit is 4mb")
        os.remove(f)
        return redirect(url_for("account"))

    # upload image into database
    update_profile_pic(session["user_id"], filename)

    flash('Upload successful!')
    return redirect(url_for("account"))
