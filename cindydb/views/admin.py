# -*- coding: utf-8 -*-
from flask import request, session, redirect, url_for, render_template, flash
import cindydb.database
import hashlib
from cindydb.forms import *
from cindydb import app
from psycopg2 import extras
import json
import cindydb.utility


@app.route('/edit-tuple', methods=['POST', 'GET'])
def edit_tuple():
        new_form = EditTuple(request.form)
        if new_form.validate():
            attributes_to_update = '(nome, cognome, data_nascita, tipo, numero_patente, sesso)'
            cond_values = (new_form.firstname_edited.data, new_form.lastname_edited.data,
                           new_form.dob_edited.data, new_form.type_edited.data, new_form.number_edited.data,
                           new_form.gender_edited.data, new_form.cf.data,)
            cindydb.database.update_query(attributes_to_update, 6, 'utenti', 'cf = %s', cond_values)
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
        schema_to_view = 'nome, cognome, cf, data_nascita, tipo, numero_patente, sesso, username'
        data = cindydb.database.select_query(schema_to_view, 'utenti', None, None)
        results = []
        columns = ('nome', 'cognome', 'cf', 'data_nascita', 'tipo', 'numero_patente', 'sesso', 'username')

        for row in data:
            results.append(dict(zip(columns, row)))
        res = json.dumps(results, default=cindydb.utility.myconverter)
        return render_template('/view-users.html', schema_to_view=schema_to_view.split(','), results=res)


@app.route('/delete-user', methods=['POST'])
def delete_user():
    for tuple in request.get_json():
        cindydb.database.delete_query('utenti', 'cf = %s', (tuple['cf'],))
    return redirect(url_for('view_users'))


@app.route('/datawarehouse')
def dw():
    if session.get('logged_in') and session.get('cf') == 'admin':
        return render_template('datawarehouse.html')
    else:
        return redirect(url_for('login'))


@app.route('/view-pl', methods=['POST', 'GET'])
def view_pl():
    if request.method == 'POST':
        old_form = EditPL(request.form)
        key = dict(request.form)['jsonval'][0]
        if key == "":
            return render_template('/edit-pl.html', form=EditPL())
        else:
            old_form = cindydb.utility.get_pl_tuple(old_form, key)
            return render_template('/edit-pl.html', form=old_form)
    else:
        schema_to_view = 'nome, latitudine, longitudine, quartiere, via, fascia_oraria'
        data = cindydb.database.select_query(schema_to_view, 'pl', None, None)
        results = []
        columns = ('nome', 'latitudine', 'longitudine', 'quartiere', 'via', 'fascia_oraria')

        for row in data:
            results.append(dict(zip(columns, row)))
        res = json.dumps(results)
        return render_template('/view-pl.html', schema_to_view=schema_to_view.split(','), results=res)


@app.route('/edit-pl', methods=['POST', 'GET'])
def edit_pl():
    new_form = EditPL(request.form)
    if new_form.validate():
        attributes_to_update = '(latitudine, longitudine, quartiere, via, fascia_oraria)'
        cond_values = (new_form.latitude.data, new_form.longitude.data,
                       new_form.district.data, new_form.street.data, new_form.time_slot.data,
                       new_form.name.data,)
        cindydb.database.update_query(attributes_to_update, 5, 'pl', 'nome = %s', cond_values)
        return redirect(url_for('view_pl'))
    else:
        return render_template('/edit-pl.html', form=new_form)


@app.route('/new-pl', methods=['POST', 'GET'])
def new_pl():
    new_form = EditPL(request.form)
    if request.method == 'POST':
        if new_form.validate():
            data = cindydb.database.select_query('*', 'pl', 'nome = %s',
                                                 (new_form.name.data,))
            if len(data) == 0:
                attributes = '(nome, latitudine, longitudine, quartiere, via, fascia_oraria)'
                cond_values = (new_form.name.data, new_form.latitude.data, new_form.longitude.data,
                               new_form.district.data, new_form.street.data, new_form.time_slot.data)
                cindydb.database.insert_query(attributes, 6, 'pl', cond_values)
                return redirect(url_for('view_pl'))
            else:
                flash('PL esistente!', category='error')
                return render_template('/new-pl.html', form=new_form)
        else:
            return render_template('/new-pl.html', form=new_form)
    return render_template('/new-pl.html', form=EditPL())


@app.route('/change-pl', methods=['POST'])
def change_pl():
    new_form = EditPL(request.form)
    if new_form.validate():
        attributes_to_update = '(latitudine, longitudine, quartiere, via, fascia_oraria)'
        cond_values = (new_form.latitude.data, new_form.longitude.data,
                       new_form.district.data, new_form.street.data, new_form.time_slot.data,
                       new_form.name.data,)
        cindydb.database.update_query(attributes_to_update, 5, 'pl', 'nome = %s', cond_values)
        return redirect(url_for('view_pl'))
    else:
        return render_template('/edit-pl.html', form=new_form)


@app.route('/delete-pl', methods=['POST'])
def delete_pl():
    for tuple in request.get_json():
        cindydb.database.delete_query('pl', 'nome = %s', (tuple['nome'],))
    return redirect(url_for('view_pl'))


@app.route('/view-ppc', methods=['POST', 'GET'])
def view_ppc():
    if request.method == 'POST':
        old_form = EditPPC(request.form)
        key = dict(request.form)['jsonval'][0]
        if key == "":
            return render_template('/edit-ppc.html', form=EditPPC())
        else:
            old_form = cindydb.utility.get_ppc_tuple(old_form, key)
            return render_template('/edit-ppc.html', form=old_form)
    else:
        schema_to_view = 'nome, latitudine, longitudine, quartiere, via, societa, telefono, email, costo_orario'
        data = cindydb.database.select_query(schema_to_view, 'ppc', None, None)
        results = []
        columns = ('nome', 'latitudine', 'longitudine', 'quartiere', 'via', 'societa', 'telefono', 'email',
                   'costo_orario')

        for row in data:
            results.append(dict(zip(columns, row)))
        res = json.dumps(results)
        return render_template('/view-ppc.html', schema_to_view=schema_to_view.split(','), results=res)


@app.route('/edit-ppc', methods=['POST', 'GET'])
def edit_ppc():
        new_form = EditPPC(request.form)
        if new_form.validate():
            attributes_to_update = '(latitudine, longitudine, quartiere, via, societa, telefono, email, costo_orario)'
            cond_values = (new_form.latitude.data, new_form.longitude.data, new_form.district.data,
                           new_form.street.data, new_form.company.data, new_form.tel.data, new_form.email.data,
                           new_form.cost.data, new_form.name.data,)
            cindydb.database.update_query(attributes_to_update, 8, 'ppc', 'nome = %s', cond_values)
            return redirect(url_for('view_ppc'))
        else:
            return render_template('/edit-ppc.html', form=new_form)


@app.route('/delete-ppc', methods=['POST'])
def delete_ppc():
    for tuple in request.get_json():
        cindydb.database.delete_query('ppc', 'nome = %s', (tuple['nome'],))
    return redirect(url_for('view_ppc'))