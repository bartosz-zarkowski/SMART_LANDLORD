# import mariadb
import pymysql
import sys
from flask import g
import os


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        # Connect to MariaDB Platform
        try:
            conn = pymysql.connect(
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASS'],
                host=os.environ['DB_HOST'],
                port=3306,
                database=os.environ['DB_DB']
            )
        except pymysql.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Get Cursor
        g.db = conn
        g.cursor = conn.cursor()

    return g.cursor, g.db


def close_db(e=None):
    """If this request connected to the database, close the connection."""
    db = g.pop("db", None)
    cursor = g.pop("cursor", None)

    if db is not None:
        db.close()
        cursor.close()
