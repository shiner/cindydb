# -*- coding: utf-8 -*-
from flask import request, session, redirect, url_for, render_template, flash
import cindydb.database
import hashlib
from cindydb.forms import *
from cindydb import app
from psycopg2 import extras
import json


@app.route('/charts')
def charts():
    if session.get('logged_in'):
        return render_template('/charts.html')
    else:
        return redirect(url_for('login'))


@app.route('/forms')
def forms():
    if session.get('logged_in'):
        return render_template('/forms.html')
    else:
        return redirect(url_for('login'))


@app.route('/tables')
def tables():
    if session.get('logged_in'):
        return render_template('/tables.html')
    else:
        return redirect(url_for('login'))


@app.route('/bootstrap-elements')
def bootstrap_elements():
    if session.get('logged_in'):
        return render_template('/bootstrap-elements.html')
    else:
        return redirect(url_for('login'))


@app.route('/blank-page')
def blank_page():
    if session.get('logged_in'):
        return render_template('/blank-page.html')
    else:
        return redirect(url_for('login'))


@app.route('/')
def index():
    # if session.get('logged_in'):
        return render_template('homepage.html', lform=Login(), form=Registration())
    # else:
    #     return redirect(url_for('login'))


# @app.route('/view-users')
# def view_users():
#     if session.get('logged_in'):
#         schema_to_view = 'nome, cognome, username, data_nascita, tel, email, sesso, residenza'
#         data = cindydb.database.select_query(schema_to_view, 'utenti', None, None)
#         return render_template('/view-users.html', schema_to_view=schema_to_view.split(','), data=data)
#     else:
#         return redirect(url_for('login'))

@app.route('/view-users')
def view_users():

        schema_to_view = 'nome, cognome, username,  tel, email, sesso, residenza'
        data = cindydb.database.select_query(schema_to_view, 'utenti', None, None)
        results = []
        columns = ('nome', 'cognome', 'username', 'tel', 'email', 'sesso', 'residenza')
        for row in data:
            results.append(dict(zip(columns, row)))
        print json.dumps(results, indent=2)
        return render_template('/view-users.html', schema_to_view=schema_to_view.split(','), results=results)
