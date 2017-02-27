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


@app.route('/pass-user', methods=['POST', 'GET'])
def pass_user_list():
    if request.method == 'POST':
        old_form = ShopPass(request.form)
        key = dict(request.form)['jsonval'][0]
        old_form = cindydb.utility.get_pass_tuple(old_form, key)
        return render_template('/shop.html', form=old_form)
    else:
        schema_to_view = 'codice, zona_ztl, durata, costo'
        data = cindydb.database.select_query(schema_to_view, 'pass', None, None)
        results = []
        columns = ('Codice', 'Zona_ZTL', 'Durata-mesi', 'Costo')
        schema_to_view = 'Codice, Zona_ZTL, Durata-mesi, Costo'
        for row in data:
            results.append(dict(zip(columns, row)))
        res = json.dumps(results)
        return render_template('/pass-user.html', schema_to_view=schema_to_view.split(','), results=res)


@app.route('/shop', methods=['POST', 'GET'])
def shop():
    new_form = ShopPass(request.form)
    new_form.auto.choices = utility.get_auto_choises()
    new_form.ppc.choices = utility.get_ppc_choises()

    id = cindydb.database.select_one_query('id_fattura', 'vendite', ' order by id_fattura desc')

    next_id = int(id[0]) + 1
    if new_form.validate():
        attributes = '(id_fattura, ppc, utente, pass, automobile, data_rilascio)'
        cond_values = (next_id , new_form.ppc.data, session.get('cf'),
                       new_form.cod.data, new_form.auto.data, new_form.date.data)
        cindydb.database.insert_query(attributes, 6, 'vendite', cond_values)
        return redirect(url_for('purchase_history'))
    else:
        return render_template('/shop.html', form=new_form)


@app.route('/purchase-history')
def purchase_history():
    schema_to_view = 'vendite.id_fattura, vendite.data_rilascio, ppc.societa, ppc.via, vendite.pass,' \
                     'pass.zona_ztl, pass.durata, vendite.automobile, automobili.marca, automobili.modello'
    query_from = 'vendite JOIN ppc ON vendite.ppc = ppc.nome JOIN utenti ON vendite.utente = utenti.cf JOIN automobili ' \
                 'ON vendite.automobile = automobili.targa JOIN pass ON vendite.pass = pass.codice'
    data = cindydb.database.select_query(schema_to_view, query_from, 'utenti.cf = %s', (session.get('cf'),))
    results = []
    columns = ('Fattura', 'Data-rilascio', 'SocietaPPC', 'ViaPPC', 'Pass', 'Zona-validita', 'Durata-mesi',
               'Nome-cliente', 'Cognome-cliente', 'Automobile', 'Marca-auto', 'Modello-auto')
    schema_to_view = 'Fattura, Data-rilascio, SocietaPPC, ViaPPC, Pass, Zona-validita, Durata-mesi, ' \
                     'Nome-cliente, Cognome-cliente, Automobile, Marca-auto, Modello-auto'
    for row in data:
        results.append(dict(zip(columns, row)))
    res = json.dumps(results, default=cindydb.utility.myconverter)
    return render_template('/purchase-history.html', schema_to_view=schema_to_view.split(','), results=res)


@app.route('/auto')
def auto():
    if session.get('logged_in'):

        attributes = 'targa, marca, modello, lunghezza, larghezza'
        data = cindydb.database.select_query(attributes, 'automobili', 'proprietario = %s',
                                             (session.get('cf'),))
        results = []
        columns = ('Targa', 'Marca', 'Modello', 'Lunghezza', 'Larghezza')
        schema_to_view = 'Targa, Marca, Modello, Lunghezza, Larghezza'
        for row in data:
            results.append(dict(zip(columns, row)))
        res = json.dumps(results)
        return render_template('/auto.html', schema_to_view=schema_to_view.split(','), results=res)


@app.route('/new-auto', methods=['POST', 'GET'])
def new_auto():
    new_form = NewAuto(request.form)
    if request.method == 'POST':
        if new_form.validate():
            data = cindydb.database.select_query('*', 'automobili', 'targa = %s',
                                                 (new_form.targa.data,))
            if len(data) == 0:
                if new_form.lung.data == '':
                    new_form.lung.data = None
                if new_form.larg.data == '':
                    new_form.larg.data = None
                attributes = '(targa, modello, marca, proprietario, lunghezza, larghezza)'
                cond_values = (new_form.targa.data, new_form.modello.data, new_form.marca.data,
                               session.get('cf'), new_form.lung.data, new_form.larg.data)
                cindydb.database.insert_query(attributes, 6, 'automobili', cond_values)
                return redirect(url_for('auto'))
            else:
                flash('Auto esistente!', category='error')
                return render_template('/new-auto.html', form=new_form)
        else:
            return render_template('/new-auto.html', form=new_form)
    return render_template('/new-auto.html', form=NewAuto())