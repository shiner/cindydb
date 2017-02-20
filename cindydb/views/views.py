# -*- coding: utf-8 -*-
from flask import request, session, redirect, url_for, render_template, flash
import cindydb.database
import hashlib
from cindydb.forms import *
from cindydb import app
from psycopg2 import extras
import json
import cindydb.utility


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
    if session.get('logged_in'):
        return render_template('homepage.html', lform=Login(), form=Registration())
    else:
        return redirect(url_for('login'))


@app.route('/edit-tuple', methods=['POST', 'GET'])
def edit_tuple():
        new_form = EditTuple(request.form)
        if new_form.validate():
            attributes_to_update = '(nome, cognome, tel, data_nascita, email, residenza, sesso)'
            cond_values = (new_form.firstname_edited.data, new_form.lastname_edited.data,
                           new_form.phonenumber_edited.data, new_form.dob_edited.data, new_form.email_edited.data,
                           new_form.city_edited.data, new_form.gender_edited.data, new_form.username.data)
            cindydb.database.update_query(attributes_to_update, 7, 'utenti', 'username = %s', cond_values)
            return redirect(url_for('view_users'))
        else:
            return render_template('/edit-tuple.html', form=new_form)


@app.route('/view-users', methods=['POST', 'GET'])
def view_users():
    if request.method == 'POST':
        old_form = EditTuple(request.form)
        key = dict(request.form)['jsonval'][0]
        old_form = cindydb.utility.get_tuple(old_form, key)
        return render_template('/edit-tuple.html', form=old_form)
    else:
        schema_to_view = 'nome, cognome, username, data_nascita, tel, email, sesso, residenza'
        data = cindydb.database.select_query(schema_to_view, 'utenti', None, None)
        results = []
        columns = ('nome', 'cognome', 'username', 'data_nascita', 'tel', 'email', 'sesso', 'residenza')

        for row in data:
            results.append(dict(zip(columns, row)))
        res = json.dumps(results, default=cindydb.utility.myconverter)
        return render_template('/view-users.html', schema_to_view=schema_to_view.split(','), results=res)


@app.route('/delete-tuple', methods=['POST'])
def delete_tuple():
    for tuple in request.get_json():
        cindydb.database.delete_query('utenti', 'username = %s', (tuple['username'],))
        return redirect(url_for('view_users'))


@app.route('/datawarehouse')
def dw():
    if session.get('logged_in') and session.get('username') == 'admin':
        return render_template('datawarehouse.html')
    else:
        return redirect(url_for('login'))