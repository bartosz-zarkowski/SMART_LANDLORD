from flask import Blueprint
from flask import render_template
from flask import g

from auth import login_required
from db import get_db

bp = Blueprint("app", __name__)


def getUserRole():
    userRole = g.user[6]
    if userRole == "tenant":
        return "najemca"
    elif userRole == "owner":
        return "właściciel"
    else:
        return "undefined"


@bp.route("/")
def index():
    return render_template("home.html")


@bp.route("/strona_glowna")
@login_required
def strona_glowna():
    return render_template("app/strona_glowna.html", userInfo=getUserRole())


@bp.route("/powiadomienia")
@login_required
def powiadomienia():
    return render_template("app/strona_glowna.html", userInfo=getUserRole())


@bp.route("/kontakty")
@login_required
def kontakty():
    return render_template("app/strona_glowna.html", userInfo=getUserRole())


@bp.route("/podsumowanie")
@login_required
def podsumowanie():
    return render_template("app/strona_glowna.html", userInfo=getUserRole())


@bp.route("/twoje_lokale")
@login_required
def twoje_lokale():
    return render_template("app/strona_glowna.html", userInfo=getUserRole())


@bp.route("/ustawienia")
@login_required
def ustawienia():
    return render_template("app/strona_glowna.html", userInfo=getUserRole())
