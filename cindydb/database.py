import psycopg2
from flask import g

conn_string = "host='localhost' dbname='db_project' user='postgres' password='frrnrt'"


def connect_db():
    """Connects to the specific database."""
    print "Connecting to database\n	->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    return cursor, conn


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        cur, conn = g._database = connect_db()
    return cur, conn


def close_connection():
    db = getattr(g, '_database', None)
    if db is not None:
        print "Close connection.\n"
        cur, conn = db
        conn.close()
