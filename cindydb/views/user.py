# -*- coding: utf-8 -*-
from flask import request, session, redirect, url_for, render_template, flash
import cindydb.database
import hashlib
from cindydb.forms import *
from cindydb import app
from psycopg2 import extras


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
        conn = cindydb.database.get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM utenti WHERE username = %s", (form.username.data, ))
        conn.commit()
        if cur.fetchone() is None:
            cur.execute("INSERT into utenti (username, psw, nome, cognome, tel, data_nascita, email, residenza, sesso) "
                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (form.username.data, hashlib.sha1(form.password.data).hexdigest(), form.firstname.data,
                            form.lastname.data, form.phonenumber.data, form.dob.data, form.email.data,
                            form.city.data, form.gender.data))
            conn.commit()
            # cindydb.database.close_connection()
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
        conn = cindydb.database.get_db()
        cur = conn.cursor()
        cur.execute("SELECT nome, cognome FROM utenti WHERE username = %s AND psw = %s ",
                       (l_form.login_user.data, hashlib.sha1(l_form.login_pass.data).hexdigest()))
        data = cur.fetchone()
        conn.commit()
        # cindydb.database.close_connection()
        if data is None:
            flash('Username o password invalida. Prova ancora!', category='error')
        else:
            flash('Login eseguito', category='success')
            session['logged_in'] = True
            session['username'] = l_form.login_user.data
            session['firstname'] = data[0]
            session['lastname'] = data[1]
            session['psw'] = hashlib.sha1(l_form.login_pass.data).hexdigest()
            return redirect(url_for('index'))

    return render_template('login.html', lform=l_form, form=Registration())


@app.route('/profile')
def profile():
    if session.get('logged_in'):
        conn = cindydb.database.get_db()
        cur = conn.cursor()
        schema = 'nome, cognome, data_nascita, tel, email, sesso, residenza, username'
        cur.execute("SELECT " + schema + " FROM utenti WHERE username = %s AND psw = %s ",
                       (session.get('username'), session.get('psw')))
        conn.commit()
        res = cur.fetchall()
        data = [attribute for attribute in res[0]]

        schema_to_view = ['Nome', 'Cognome', 'Data di nascita', 'Telefono', 'Email', 'Sesso', 'Residenza', 'Username']
        return render_template('/profile.html', data=zip(schema_to_view, data), gender=data[5])
    else:
        return redirect(url_for('login'))


@app.route('/edit-profile', methods=['GET', 'POST'])
def editprofile():
    if session.get('logged_in'):
        old_form = Edit(request.form)
        old_form = cindydb.database.get_profile(old_form, session.get('username'))
        if request.method == 'POST':
            new_form = Edit(request.form)
            if new_form.validate():
                conn = cindydb.database.get_db()
                cur = conn.cursor()
                cur.execute(
                    "UPDATE utenti SET (nome, cognome, tel, data_nascita, email, residenza, sesso) = ( %s, %s, %s, %s, %s, %s, %s ) "
                    "WHERE username = %s", \
                    (new_form.firstname_edited.data, new_form.lastname_edited.data, new_form.phonenumber_edited.data, new_form.dob_edited.data,
                     new_form.email_edited.data, new_form.city_edited.data, new_form.gender_edited.data,
                     session.get('username')))
                conn.commit()
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
                conn = cindydb.database.get_db()
                cur = conn.cursor()
                dict_cur = conn.cursor(cursor_factory=extras.DictCursor)
                dict_cur.execute("SELECT psw FROM utenti WHERE username = %s", (session.get('username'),))
                res = dict_cur.fetchone()
                conn.commit()
                if res['psw'] == hashlib.sha1(form_change_psw.oldpassword.data).hexdigest():
                    cur.execute(
                        "UPDATE utenti SET psw = %s WHERE username = %s",
                        (hashlib.sha1(form_change_psw.newpassword.data).hexdigest(), session.get('username')))
                    conn.commit()
                    flash('Password modificata', category='success')
                    session['psw'] = hashlib.sha1(form_change_psw.newpassword.data).hexdigest()
                else:
                    flash('Password attuale non corretta', category='warning')
                    return render_template('/change-password.html', form=form_change_psw)
            if not form_change_psw.validate():
                flash('Non sono state apportate modifiche', category='warning')
            return redirect(url_for('profile'))
        return render_template('/change-password.html', form=form_change_psw)
    else:
        return redirect(url_for('login'))


 # cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND "
        #                "table_name='utenti'")
        # conn.commit()
        # schema_to_view = cursor.fetchall()
