import psycopg2
from flask import g
from cindydb import app

conn_string = "host='localhost' dbname='db_project' user='postgres' password='frrnrt'"


def connect_db():
    """Connects to the specific database."""
    print "Connecting to database\n	->%s" % conn_string
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


def get_profile(form, username):
    conn = get_db()
    cur = conn.cursor()
    schema = 'nome, cognome, data_nascita, tel, email, sesso, residenza'
    cur.execute("SELECT " + schema + " FROM utenti WHERE username = %s",
                   (username, ))
    conn.commit()
    res = cur.fetchall()
    form.firstname_edited.data = res[0][0]
    form.lastname_edited.data = res[0][1]
    form.phonenumber_edited.data = res[0][3]
    form.dob_edited.data = res[0][2]
    form.gender_edited.data = res[0][5]
    form.city_edited.data = res[0][6]
    form.email_edited.data = res[0][4]
    return form