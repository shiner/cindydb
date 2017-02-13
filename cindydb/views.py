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


@app.route('/login')
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
            cursor.execute("INSERT into utenti (username, psw, nome, cognome, tel, data_nascita, email) "
                           "VALUES (%s, %s, %s, %s,%s,%s,%s)",
                           (form.username.data, hashlib.sha1(form.password.data).hexdigest(), form.firstname.data,
                            form.lastname.data, form.phonenumber.data, form.dob.data, form.email.data))
            conn.commit()
            database.close_connection()
            flash('Grazie per esserti registrato', category='success')
            session['logged_in'] = True
            session['username'] = form.username.data
            session['firstname'] = form.firstname.data
            session['lastname'] = form.lastname.data
            session['password'] = hashlib.sha1(form.password.data).hexdigest()
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
        rec = cursor.fetchone()
        conn.commit()
        database.close_connection()
        if rec is None:
            flash('Username o password invalida. Prova ancora!', category='error')
        else:
            flash('Login eseguito', category='success')
            session['logged_in'] = True
            session['username'] = l_form.login_user.data
            session['firstname'] = rec[0]
            session['lastname'] = rec[1]
            session['password'] = hashlib.sha1(l_form.login_pass.data).hexdigest()
            return redirect(url_for('index'))

    return render_template('login.html', lform=l_form, form=Registration())


@app.route('/')
def index():
    if session.get('logged_in'):
        return render_template('homepage.html', lform=Login(), form=Registration())
    else:
        return redirect(url_for('login'))
