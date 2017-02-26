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
        # return redirect(url_for('login'))
        session['logged_in'] = False
        return render_template('homepage.html', lform=Login(), form=Registration())