import psycopg2
from flask import g
import forms

conn_string = "host='localhost' dbname='db_project' user='postgres' password='frrnrt'"


def connect_db():
    """Connects to the specific database."""
    print "Connecting to database\n	->%s" % (conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    return cursor, conn


def close_connection():
    db = getattr(g, '_database', None)
    if db is not None:
        print "Close connection.\n"
        cur, conn = db
        conn.close()


def get_profile(form, username):
    cursor, conn = connect_db()
    schema = 'nome, cognome, data_nascita, tel, email, sesso, residenza'
    cursor.execute("SELECT " + schema + " FROM utenti WHERE username = %s",
                   (username, ))
    conn.commit()
    res = cursor.fetchall()
    close_connection()
    form.firstname_edited.data = res[0][0]
    form.lastname_edited.data = res[0][1]
    form.phonenumber_edited.data = res[0][3]
    form.dob_edited.data = res[0][2]
    form.gender_edited.data = res[0][5]
    form.city_edited.data = res[0][6]
    form.email_edited.data = res[0][4]
    return form