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
    cur.execute("UPDATE " + table + " SET " + attributes + " = " + s + " WHERE " + condition, cond_values)
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


def select_one_query(attributes, table, condition):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT " + attributes + " FROM " + table + condition)
    conn.commit()
    res = cur.fetchone()
    return res


def booking_query(lung, larg, di, df):
    conn = get_db()
    cur = conn.cursor()
    query = '(SELECT posti_auto.ppc, posti_auto.numero, optional.stato, posti_auto.lunghezza, posti_auto.larghezza ' \
            'FROM posti_auto LEFT OUTER JOIN optional ON posti_auto.numero = optional.posto_auto ' \
            'AND posti_auto.ppc = optional.ppc ' \
            'WHERE (posti_auto.ppc, posti_auto.numero) NOT IN (SELECT optional.ppc, optional.posto_auto ' \
            'FROM optional WHERE optional.stato = \'occupato\') ' \
            'AND posti_auto.lunghezza >= %s AND posti_auto.larghezza >= %s ) ' \
            'EXCEPT ' \
            '(SELECT posti_auto.ppc, posti_auto.numero, optional.stato, posti_auto.lunghezza, posti_auto.larghezza ' \
            'FROM posti_auto JOIN soste_passate ON soste_passate.ppc = posti_auto.ppc AND soste_passate.posto_auto = ' \
            'posti_auto.numero ' \
            'FULL OUTER JOIN optional ON posti_auto.numero = optional.posto_auto AND posti_auto.ppc = optional.ppc ' \
            'WHERE (%s >= soste_passate.data_inizio AND %s <= soste_passate.data_fine) OR ' \
            '(%s < soste_passate.data_inizio AND %s > ' \
            'soste_passate.data_fine) OR (%s < soste_passate.data_fine) ' \
            'UNION ' \
            'SELECT posti_auto.ppc, posti_auto.numero, optional.stato, posti_auto.lunghezza, posti_auto.larghezza ' \
            'FROM posti_auto JOIN soste ON soste.ppc = posti_auto.ppc AND soste.posto_auto = posti_auto.numero ' \
            'FULL OUTER JOIN optional ON posti_auto.numero = optional.posto_auto AND posti_auto.ppc = optional.ppc ' \
            'WHERE (%s >= soste.data_inizio AND %s <= soste.data_fine) OR (%s < soste.data_inizio AND %s > ' \
            'soste.data_fine) OR (%s < soste.data_fine))'

    cur.execute(query, (lung, larg, di, df, di, df, di, di, df, di, df, di, ))

    conn.commit()
    res = cur.fetchall()
    return res



