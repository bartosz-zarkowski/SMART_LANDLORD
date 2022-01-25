import mariadb
import sys
from flask import g
import os
from dotenv import load_dotenv

load_dotenv()


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        # Connect to MariaDB Platform
        try:
            conn = mariadb.connect(
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASS'),
                host=os.getenv('DB_HOST'),
                port=3306,
                database=os.getenv('DB_DB')
            )
        except mariadb.Error as e:
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
