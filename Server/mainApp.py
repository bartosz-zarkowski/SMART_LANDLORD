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


def getUserName():
    firstName = g.user[2]
    fullName = g.user[3]
    name = firstName + " " + fullName
    initials = firstName[0] + fullName[0]
    return name, initials


@bp.route("/")
def index():
    return render_template("home.html")


@bp.route("/strona_glowna")
@login_required
def strona_glowna():
    name, initials = getUserName()
    return render_template(
        "app/strona_glowna.html",
        userInfo=getUserRole(),
        name=name,
        initials=initials,
        title="Strona Główna"
    )


@bp.route("/powiadomienia")
@login_required
def powiadomienia():
    name, initials = getUserName()
    return render_template(
        "app/strona_glowna.html",
        userInfo=getUserRole(),
        name=name,
        initials=initials,
        title="Powiadomienia"
    )


@bp.route("/kontakty")
@login_required
def kontakty():
    name, initials = getUserName()
    return render_template(
        "app/strona_glowna.html",
        userInfo=getUserRole(),
        name=name,
        initials=initials,
        title="Kontakty"
    )


@bp.route("/podsumowanie")
@login_required
def podsumowanie():
    name, initials = getUserName()
    return render_template(
        "app/strona_glowna.html",
        userInfo=getUserRole(),
        name=name,
        initials=initials,
        title="Podsumowanie"
    )


@bp.route("/twoje_lokale")
@login_required
def twoje_lokale():
    name, initials = getUserName()
    return render_template(
        "app/twoje_lokale.html",
        userInfo=getUserRole(),
        name=name,
        initials=initials,
        title="Twoje lokale"
    )


@bp.route("/dodaj_lokal")
@login_required
def ustawienia():
    name, initials = getUserName()
    return render_template(
        "app/strona_glowna.html",
        userInfo=getUserRole(),
        name=name,
        initials=initials,
        title="Dodaj lokal"
    )


@bp.route("/ustawienia")
@login_required
def ustawienia():
    name, initials = getUserName()
    return render_template(
        "app/strona_glowna.html",
        userInfo=getUserRole(),
        name=name,
        initials=initials,
        title="Ustawienia"
    )
