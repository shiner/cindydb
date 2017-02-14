# -*- coding: utf-8 -*-
from flask import request, session, redirect, url_for, render_template, flash
import database
import hashlib
from forms import Login, Registration
from cindydb import app


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
        cursor, conn = database.get_db()
        cursor.execute("SELECT * FROM utenti WHERE username = %s", (form.username.data, ))
        conn.commit()
        if cursor.fetchone() is None:
            cursor.execute("INSERT into utenti (username, psw, nome, cognome, tel, data_nascita, email, residenza, sesso) "
                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (form.username.data, hashlib.sha1(form.password.data).hexdigest(), form.firstname.data,
                            form.lastname.data, form.phonenumber.data, form.dob.data, form.email.data,
                            form.city.data, form.gender.data))
            conn.commit()
            database.close_connection()
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
        cursor, conn = database.get_db()
        cursor.execute("SELECT nome, cognome FROM utenti WHERE username = %s AND psw = %s ",
                       (l_form.login_user.data, hashlib.sha1(l_form.login_pass.data).hexdigest()))
        data = cursor.fetchone()
        conn.commit()
        database.close_connection()
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


@app.route('/')
def index():
    if session.get('logged_in'):
        return render_template('homepage.html', lform=Login(), form=Registration())
    else:
        return redirect(url_for('login'))


@app.route('/view-table')
def view_table():
    if session.get('logged_in'):
        cursor, conn = database.get_db()
        schema_to_view = 'nome, cognome, username, data_nascita, tel, email, sesso, residenza'
        cursor.execute("SELECT " + schema_to_view + " FROM utenti")
        conn.commit()
        data = cursor.fetchall()
        database.close_connection()
        print schema_to_view.split(','), data
        return render_template('/view-table.html', schema_to_view=schema_to_view.split(','), data=data)
    else:
        return redirect(url_for('login'))


@app.route('/profile')
def profile():
    if session.get('logged_in'):
        cursor, conn = database.get_db()
        schema = 'nome, cognome, data_nascita, tel, email, sesso, residenza, username'
        cursor.execute("SELECT " + schema + " FROM utenti WHERE username = %s AND psw = %s ",
                       (session.get('username'), session.get('psw')))
        conn.commit()
        res = cursor.fetchall()
        database.close_connection()
        data = [attribute for attribute in res[0]]

        schema_to_view = ['Nome', 'Cognome', 'Data di nascita', 'Telefono', 'Email', 'Sesso', 'Residenza', 'Username']
        return render_template('/profile.html', data=zip(schema_to_view, data), gender=data[5])
    else:
        return redirect(url_for('login'))


@app.route('/edit-profile')
def edit_profile():
    if session.get('logged_in'):
        return render_template('/profile.html', data=zip(schema_to_view, data), gender=data[5])
    else:
        return redirect(url_for('login'))



 # cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND "
        #                "table_name='utenti'")
        # conn.commit()
        # schema_to_view = cursor.fetchall()
