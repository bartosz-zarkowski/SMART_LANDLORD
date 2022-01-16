from flask import Blueprint
from flask import render_template

from auth import login_required
from db import get_db

bp = Blueprint("app", __name__)


@bp.route("/")
def index():
    return render_template("home.html")


@bp.route("/strona_glowna")
@login_required
def strona_glowna():
    return render_template("app/strona_glowna_najemca.html")

