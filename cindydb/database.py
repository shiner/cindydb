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


def get_profile(form, username, psw):
    cursor, conn = connect_db()
    schema = 'nome, cognome, data_nascita, tel, email, sesso, residenza'
    cursor.execute("SELECT " + schema + " FROM utenti WHERE username = %s AND psw = %s ",
                   (username, psw))
    conn.commit()
    res = cursor.fetchall()
    close_connection()
    form.firstname.data = res[0][0]
    form.lastname.data = res[0][1]
    form.phonenumber.data = res[0][3]
    form.dob.data = res[0][2]
    form.gender.data = res[0][5]
    form.city.data = res[0][6]
    form.username.data = username
    form.email.data = res[0][4]
    form.password.data = res[0][4]
    form.email.data = res[0][4]
    return form