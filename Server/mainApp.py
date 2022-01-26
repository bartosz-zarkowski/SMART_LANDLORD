from flask import Blueprint, jsonify
from flask import render_template
from flask import g
from flask import request
from flask import flash
from flask import redirect
from flask import url_for

from db import get_db
from auth import login_required

bp = Blueprint("app", __name__)


def getUserRole():
    userRole = g.user[5]
    if userRole == "tenant":
        return "najemca"
    elif userRole == "owner":
        return "właściciel"
    else:
        return "undefined"


def getUserName():
    firstName = g.user[1]
    fullName = g.user[2]
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
    userPermission = getUserRole()
    cursor, db = get_db()

    if userPermission != "właściciel":
        cursor.execute("SELECT l.city, l.street, l.localNumber FROM users as `u` "
                       "JOIN locals as `l` on u.localCode = l.localCode WHERE userId = %s;", (g.user[0],))
        userLocal = cursor.fetchall()

        return render_template(
            "app/strona_glowna.html",
            userInfo=userPermission,
            name=name,
            initials=initials,
            title="Strona Główna",
            local=userLocal[0]
        )
    else:
        cursor.execute("SELECT count(*) FROM locals WHERE ownerId = %s", (g.user[0],))
        numberOfLocals = cursor.fetchall()

        cursor.execute("SELECT count(*) FROM users as `u` "
                       "JOIN locals as `l` on u.localCode = l.localCode WHERE l.ownerId = %s;", (g.user[0],))
        numberOfTenants = cursor.fetchall()

        return render_template(
            "app/strona_glowna.html",
            userInfo=userPermission,
            name=name,
            initials=initials,
            title="Strona Główna",
            numberOfLocals=numberOfLocals,
            numberOfTenants=numberOfTenants
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


@bp.route("/twoje_lokale", methods=("GET", "PATCH"))
@login_required
def twoje_lokale():
    name, initials = getUserName()
    userPermission = getUserRole()
    if userPermission != "właściciel":
        return render_template(
            "app/403.html",
            userInfo=userPermission,
            name=name,
            initials=initials,
            title="403 - Nie masz uprawnień"
        )
    else:
        cursor, db = get_db()

        cursor.execute("SELECT city, street, localNumber, localCode, localId, leasePrice, dueDay "
                       "FROM locals WHERE ownerId = %s", (g.user[0],))
        currentOwnerLocals = cursor.fetchall()

        cursor.execute("SELECT name, fullName, phoneNumber, u.localCode FROM users as `u` "
                       "JOIN locals as `l` on u.localCode = l.localCode WHERE l.ownerId = %s;", (g.user[0],))
        tenants = cursor.fetchall()

        cursor.execute("SELECT s.localId, IF((SUM(status)<COUNT(status)), 0, 1) as 'localStatus' FROM sensors as `s` "
                       "JOIN locals as `l` ON s.localId=l.localId "
                       "WHERE l.ownerId=%s "
                       "GROUP BY s.localId", (g.user[0],))
        localsStatuses = cursor.fetchall()
        print(localsStatuses)

        return render_template(
            "app/twoje_lokale.html",
            userInfo=userPermission,
            name=name,
            initials=initials,
            title="Twoje lokale",
            locals=currentOwnerLocals,
            localsStatuses=localsStatuses,
            tenants=tenants
        )


@bp.route("/dodaj_lokal", methods=("GET", "POST"))
@login_required
def dodaj_lokal():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        city = request.form["city"]
        street = request.form["street"]
        localNumber = request.form["localNumber"]
        localCode = request.form["localCode"]
        dueDay = request.form["dueDay"]
        leasePrice = request.form["leasePrice"]
        cursor, db = get_db()
        error = None

        if not city:
            error = "City is required."
        elif not street:
            error = "Street is required."
        elif not localNumber:
            error = "Local number is required."
        elif not localCode:
            error = "Local Code is required."
        elif not dueDay:
            error = "Due day is required."
        elif not leasePrice:
            error = "Lease price is required."

        if error is None:
            try:
                cursor.execute(
                    "INSERT INTO locals (ownerId, city, street, localNumber, localCode, dueDay, leasePrice) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (g.user[0], city, street, localNumber, localCode, dueDay, leasePrice),
                )
                db.commit()

                cursor.execute("SELECT localId FROM locals WHERE localCode=%s", (localCode,))
                newLocalId = cursor.fetchall()

                cursor.execute("INSERT INTO sensors (localId, status) VALUES (%s, %s)", (newLocalId[0][0], 1))
                db.commit()

            except db.IntegrityError:
                flash("Lokal z takim kodem już istnieje, spróbuj ponownie", 'danger')
            else:
                flash("Pomyślnie dodano nowy lokal!", 'success')

        else: flash(error)

    name, initials = getUserName()
    userPermission = getUserRole()
    if userPermission != "właściciel":
        return render_template(
            "app/403.html",
            userInfo=userPermission,
            name=name,
            initials=initials,
            title="403 - Nie masz uprawnień"
        )
    else:
        return render_template(
            "app/dodaj_lokal.html",
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


@bp.route('/update_local', methods=("PATCH",))
@login_required
def create():
    json = request.json

    local_code = json['local_code']
    kwota_najmu = json['kwota_najmu']
    termin_platnosci = json['termin_platnosci']

    cursor, db = get_db()
    cursor.execute(
        "UPDATE locals SET leasePrice=%s, dueDay=%s WHERE localCode=%s",
        (kwota_najmu, termin_platnosci, local_code),
    )
    db.commit()

    return redirect(url_for("app.twoje_lokale"))

