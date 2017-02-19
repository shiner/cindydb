# -*- coding: utf-8 -*-
from flask import request, session, redirect, url_for, render_template, flash
import cindydb.database
import hashlib
from cindydb.forms import *
from cindydb import app
from psycopg2 import extras
import cindydb.utility


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
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
        data = cindydb.database.select_query('*', 'utenti', 'username = %s', (form.username.data, ))
        if len(data) == 0:
            attributes = '(username, psw, nome, cognome, tel, data_nascita, email, residenza, sesso)'
            cond_values = (form.username.data, hashlib.sha1(form.password.data).hexdigest(), form.firstname.data,
                           form.lastname.data, form.phonenumber.data, form.dob.data, form.email.data,
                           form.city.data, form.gender.data)
            cindydb.database.insert_query(attributes, 9, 'utenti', cond_values)

            flash('Grazie per esserti registrato', category='success')
            session['logged_in'] = True
            session['username'] = form.username.data
            session['firstname'] = form.firstname.data
            session['lastname'] = form.lastname.data
            session['psw'] = hashlib.sha1(form.password.data).hexdigest()
            return redirect(url_for('index'))
        else:
            flash('Username esistente', category='error')

    return render_template('register.html', lform=Login(), form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    l_form = Login(request.form)
    if request.method == 'POST' and l_form.validate():
        data = cindydb.database.select_query('nome, cognome', 'utenti', 'username = %s AND psw = %s',
                                             (l_form.login_user.data, hashlib.sha1(l_form.login_pass.data).hexdigest()))
        if len(data) == 0:
            flash('Username o password invalida. Prova ancora!', category='error')
        else:
            flash('Login eseguito', category='success')
            session['logged_in'] = True
            session['username'] = l_form.login_user.data
            session['firstname'] = data[0][0]
            session['lastname'] = data[0][1]
            session['psw'] = hashlib.sha1(l_form.login_pass.data).hexdigest()
            return redirect(url_for('index'))

    return render_template('login.html', lform=l_form, form=Registration())


@app.route('/profile')
def profile():
    if session.get('logged_in'):
        attributes = 'nome, cognome, data_nascita, tel, email, sesso, residenza, username'
        data = cindydb.database.select_query(attributes, 'utenti', 'username = %s AND psw = %s',
                                             (session.get('username'), session.get('psw')))
        attr = [attribute for attribute in data[0]]
        schema_to_view = ['Nome', 'Cognome', 'Data di nascita', 'Telefono', 'Email', 'Sesso', 'Residenza', 'Username']
        return render_template('/profile.html', data=zip(schema_to_view, attr), gender=attr[5])
    else:
        return redirect(url_for('login'))


@app.route('/edit-profile', methods=['GET', 'POST'])
def editprofile():
    if session.get('logged_in'):
        old_form = Edit(request.form)
        old_form = cindydb.utility.get_profile(old_form, (session.get('username'),))
        if request.method == 'POST':
            new_form = Edit(request.form)
            if new_form.validate():
                attributes_to_update = '(nome, cognome, tel, data_nascita, email, residenza, sesso)'
                cond_values = (new_form.firstname_edited.data, new_form.lastname_edited.data,
                               new_form.phonenumber_edited.data, new_form.dob_edited.data, new_form.email_edited.data,
                               new_form.city_edited.data, new_form.gender_edited.data, session.get('username'))
                cindydb.database.update_query(attributes_to_update, 7, 'utenti', 'username = %s', cond_values)
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
