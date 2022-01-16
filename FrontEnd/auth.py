import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")
    cursor, db = get_db()

    if user_id is None:
        g.user = None
    else:
        cursor.execute("SELECT * FROM users WHERE userId = %s", (user_id,))
        user = cursor.fetchall()
        g.user = (user[0])


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        name = request.form["name"]
        fullName = request.form["fullName"]
        email = request.form["email"]
        password = request.form["password"]
        cursor, db = get_db()
        error = None

        if not email:
            error = "Email is required."
        elif not password:
            error = "Password is required."
        elif not name:
            error = "Name is required."
        elif not fullName:
            error = "Ful name is required."

        if error is None:
            try:
                cursor.execute(
                    "INSERT INTO users (name, fullName, email, password) VALUES (%s, %s, %s, %s)",
                    (name, fullName, email, generate_password_hash(password)),
                )
                db.commit()
            except cursor.IntegrityError:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"User with email {email} is already registered."
            else:
                # Success, go to the login page.
                return redirect(url_for("auth.login"))

        flash(error)
        print(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cursor, db = get_db()
        error = None

        cursor.execute("SELECT userId, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchall()

        userId = user[0][0]
        userPassword = user[0][1]

        if email is None:
            error = "Incorrect email."
        elif not check_password_hash(userPassword, password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = userId
            return redirect(url_for("app.strona_glowna"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("landing"))
