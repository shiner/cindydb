# -*- coding: utf-8 -*-
from flask import request, session, redirect, url_for, render_template, flash
import cindydb.database
from cindydb import app
import cindydb.utility
import json


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
    data = cindydb.database.select_query(schema_to_query, query_from, 'posti_auto.ppc = %s', (key,))
    results = []
    columns = ('Numero', 'Lunghezza', 'Larghezza', 'Stato', 'Azienda-sensore', 'Modello-sensore')
    schema_to_view = 'Numero, Lunghezza, Larghezza, Stato, Azienda-sensore, Modello-sensore'
    for row in data:
        results.append(dict(zip(columns, row)))
    res = json.dumps(results)
    return render_template('/view-parking-spaces.html', schema_to_view=schema_to_view.split(','), results=res)