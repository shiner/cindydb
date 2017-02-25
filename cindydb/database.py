import psycopg2
from flask import g
from cindydb import app

conn_string = "host='localhost' dbname='db_parking' user='postgres' password='frrnrt'"


def connect_db():
    """Connects to the specific database."""
    print "Connecting to database..."
    conn = psycopg2.connect(conn_string)
    return conn


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, '_database'):
        g._database = connect_db()
    return g._database


@app.teardown_appcontext
def close_connection(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, '_database'):
        g._database.close()


def select_query(attributes, table, condition, cond_values):
    conn = get_db()
    cur = conn.cursor()
    if condition:
        cur.execute("SELECT " + attributes + " FROM " + table + " WHERE " + condition, cond_values)
    else:
        cur.execute("SELECT " + attributes + " FROM " + table)
    conn.commit()
    res = cur.fetchall()
    return res


def update_query(attributes, n, table, condition, cond_values):
    s = '(' + '%s, ' * (n - 1) + '%s )'
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE " + table + " SET " + attributes + " = " + s + "WHERE " + condition, cond_values)
    conn.commit()


def insert_query(attributes, n, table, cond_values):
    s = '(' + '%s, ' * (n - 1) + '%s )'
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO " + table + " " + attributes + " VALUES " + s, cond_values)
    conn.commit()


def delete_query(table, condition, cond_values):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM " + table + " WHERE " + condition, cond_values)
    conn.commit()
