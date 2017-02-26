# -*- coding: utf-8 -*-
from flask import request, session, redirect, url_for, render_template, flash
import cindydb.database
import hashlib
from cindydb.forms import *
from cindydb import app
from psycopg2 import extras
import cindydb.utility
import json


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    if session['logged_in'] == True:
        session.pop('logged_in', None)
        session.pop('username', None)
        session.pop('firstname', None)
        session.pop('lastname', None)
        l_form = Login(request.form)
        return render_template('login.html', lform=l_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Registration(request.form)
    if request.method == 'POST' and form.validate():
        data = cindydb.database.select_query('*', 'utenti', 'cf = %s OR username = %s',
                                             (form.cf.data, form.username.data,))
        if len(data) == 0:
            attributes = '(cf, nome, cognome, data_nascita, tipo, numero_patente, sesso, username, psw)'
            cond_values = (form.cf.data, form.firstname.data, form.lastname.data, form.dob.data, form.type.data,
                           form.number.data, form.gender.data, form.username.data,
                           hashlib.sha1(form.password.data).hexdigest(),)
            cindydb.database.insert_query(attributes, 9, 'utenti', cond_values)

            # flash('Grazie per esserti registrato', category='success')
            session['logged_in'] = True
            session['username'] = form.username.data
            session['firstname'] = form.firstname.data
            session['lastname'] = form.lastname.data
            session['psw'] = hashlib.sha1(form.password.data).hexdigest()
            session['cf'] = form.cf.data
            return redirect(url_for('login'))
        else:
            flash('Username gia\' utilizzata!', category='error')

    return render_template('register.html', lform=Login(), form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    l_form = Login(request.form)
    if request.method == 'POST' and l_form.validate():
        data = cindydb.database.select_query('cf, nome, cognome', 'utenti', 'username = %s AND psw = %s',
                                             (l_form.login_user.data, hashlib.sha1(l_form.login_pass.data).hexdigest()))
        if len(data) == 0:
            flash('Username o password invalida. Prova ancora!', category='error')
        else:
            flash('Login eseguito', category='success')
            session['logged_in'] = True
            session['username'] = l_form.login_user.data
            session['cf'] = data[0][0]
            session['firstname'] = data[0][1]
            session['lastname'] = data[0][2]
            session['psw'] = hashlib.sha1(l_form.login_pass.data).hexdigest()
            return redirect(url_for('index'))
    return render_template('login.html', lform=l_form, form=Registration())


@app.route('/profile')
def profile():
    if session.get('logged_in'):
        attributes = 'nome, cognome, cf, data_nascita, tipo, numero_patente, sesso, username, psw'
        data = cindydb.database.select_query(attributes, 'utenti', 'cf = %s',
                                             (session.get('cf'),))
        attr = [attribute for attribute in data[0]]
        attr[2] = attr[2].upper()
        if attr[4] == 'up':
            attr[4] = 'Utente premium'
        else:
            attr[4] = 'Utente abbonato'
        schema_to_view = ['Nome', 'Cognome', 'Codice fiscale', 'Data di nascita', 'Tipo', 'Numero di patente', 'Sesso', 'Username']
        return render_template('/profile.html', data=zip(schema_to_view, attr), gender=attr[6])
    else:
        return redirect(url_for('login'))


@app.route('/edit-profile', methods=['GET', 'POST'])
def editprofile():
    if session.get('logged_in'):
        old_form = Edit(request.form)
        old_form = cindydb.utility.get_profile(old_form, (session.get('cf'),))
        if request.method == 'POST':
            new_form = Edit(request.form)
            if new_form.validate():
                attributes_to_update = '(nome, cognome, data_nascita, tipo, numero_patente, sesso)'
                cond_values = (new_form.firstname_edited.data, new_form.lastname_edited.data,
                               new_form.dob_edited.data, new_form.type_edited.data, new_form.number_edited.data,
                               new_form.gender_edited.data, session.get('cf'),)
                cindydb.database.update_query(attributes_to_update, 6, 'utenti', 'cf = (%s)', cond_values)
                flash('Profilo aggiornato', category='success')
                session['firstname'] = new_form.firstname_edited.data
                session['lastname'] = new_form.lastname_edited.data
            else:
                return render_template('/edit-profile.html', form=new_form)
            return redirect(url_for('profile'))
        else:
            return render_template('/edit-profile.html', form=old_form)
    else:
        return redirect(url_for('login'))


@app.route('/change-password', methods=['GET', 'POST'])
def changepassword():
    if session.get('logged_in'):
        form_change_psw = ChangePassword(request.form)
        if request.method == 'POST':
            if form_change_psw.validate():
                res = cindydb.database.select_query('psw', 'utenti', 'username = %s', (session.get('username'),))
                if res[0][0] == hashlib.sha1(form_change_psw.oldpassword.data).hexdigest():
                    condition = (hashlib.sha1(form_change_psw.newpassword.data).hexdigest(), session.get('username'))
                    cindydb.database.update_query('psw', 1, 'utenti', 'username = %s', condition)
                    flash('Password modificata', category='success')
                    session['psw'] = hashlib.sha1(form_change_psw.newpassword.data).hexdigest()
                else:
                    return render_template('/change-password.html', form=form_change_psw, message='Password attuale non corretta')
            if not form_change_psw.validate():
                return render_template('/change-password.html', form=form_change_psw)
            return redirect(url_for('profile'))
        return render_template('/change-password.html', form=form_change_psw)
    else:
        return redirect(url_for('login'))


 # cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND "
        #                "table_name='utenti'")
        # conn.commit()
        # schema_to_view = cursor.fetchall()


@app.route('/view-pl-users')
def view_pl_users():
    schema_to_view = 'nome, latitudine, longitudine, quartiere, via, fascia_oraria'
    data = cindydb.database.select_query(schema_to_view, 'pl', None, None)
    results = []
    columns = ('Nome', 'Latitudine', 'Longitudine', 'Quartiere', 'Via', 'Fascia-oraria')
    schema_to_view = 'Nome, Latitudine, Longitudine, Quartiere, Via, Fascia-oraria'
    for row in data:
        results.append(dict(zip(columns, row)))
    res = json.dumps(results)
    return render_template('/view-pl-users.html', schema_to_view=schema_to_view.split(','), results=res)


@app.route('/view-ppc-users')
def view_ppc_users():
    schema_to_view = 'nome, latitudine, longitudine, quartiere, via, societa, telefono, email, costo_orario'
    data = cindydb.database.select_query(schema_to_view, 'ppc', None, None)
    results = []
    columns = ('Nome', 'Latitudine', 'Longitudine', 'Quartiere', 'Via', 'Societa\'', 'Telefono', 'Email',
               'Costo-orario')
    schema_to_view = 'Nome, Latitudine, Longitudine, Quartiere, Via, Societa\', Telefono, Email, Costo-orario'
    for row in data:
        results.append(dict(zip(columns, row)))
    res = json.dumps(results)
    return render_template('/view-ppc-users.html', schema_to_view=schema_to_view.split(','), results=res)


@app.route('/view-parking-spaces', methods=['POST', 'GET'])
def view_parking_spaces():
    key = dict(request.form)['jsonval'][0]
    schema_to_query = 'posti_auto.numero, posti_auto.lunghezza, posti_auto.larghezza, optional.stato, sensori.azienda, ' \
                      'sensori.modello'
    query_from = 'optional FULL OUTER JOIN posti_auto ON posti_auto.ppc = optional.ppc AND posti_auto.numero ' \
                 '= optional.posto_auto ' \
                 'FULL OUTER JOIN sensori ON optional.sensore = sensori.id'
    data = cindydb.database.select_query(schema_to_query, query_from, 'posti_auto.ppc = %s', key)
    results = []
    columns = ('Numero', 'Lunghezza', 'Larghezza', 'Stato', 'Azienda-sensore', 'Modello-sensore')
    schema_to_view = 'Numero, Lunghezza, Larghezza, Stato, Azienda-sensore, Modello-sensore'
    for row in data:
        results.append(dict(zip(columns, row)))
    res = json.dumps(results)
    return render_template('/view-parking-spaces.html', schema_to_view=schema_to_view.split(','), results=res)

