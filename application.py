from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import datetime

from helpers import *

# configure application
app = Flask(__name__)

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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profile")
def profile():
    """Show profile"""

    # get username
    username = get_username(session["user_id"])

    return render_template("profile.html", name=username[0]["username"])


@app.route("/search/<username>", methods=["GET", "POST"])
def search(username):
    """Search for user"""

    # check if username exists
    if len(check_username(username)) != 1:
        flash('Gebruikersnaam bestaat niet!')
        return render_template("index.html")

    return render_template("profile.html", name=username)


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
        return redirect(url_for("index"))

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