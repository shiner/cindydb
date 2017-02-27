import cindydb.database
import datetime
from flask import session

def myconverter(o):
    if isinstance(o, datetime.date):
        return o.__str__()


def get_profile(edit_form, cf):
    schema_to_view = 'nome, cognome, data_nascita, tipo, numero_patente, sesso'
    res = cindydb.database.select_query(schema_to_view, 'utenti', 'cf = %s', cf)
    edit_form.firstname_edited.data = res[0][0]
    edit_form.lastname_edited.data = res[0][1]
    edit_form.dob_edited.data = res[0][2]
    edit_form.type_edited.data = res[0][3]
    edit_form.number_edited.data = res[0][4]
    edit_form.gender_edited.data = res[0][5]
    return edit_form


def get_tuple(edit_tuple_form, key):
    schema_to_view = 'username, nome, cognome, data_nascita, tipo, numero_patente, sesso'
    res = cindydb.database.select_query(schema_to_view, 'utenti', 'cf = %s', (key,))
    edit_tuple_form.cf.data = key
    edit_tuple_form.username.data = res[0][0]
    edit_tuple_form.firstname_edited.data = res[0][1]
    edit_tuple_form.lastname_edited.data = res[0][2]
    edit_tuple_form.dob_edited.data = res[0][3]
    edit_tuple_form.type_edited.data = res[0][4]
    edit_tuple_form.number_edited.data = res[0][5]
    edit_tuple_form.gender_edited.data = res[0][6]
    return edit_tuple_form


def get_pl_tuple(edit_pl_form, key):
    schema_to_view = 'latitudine, longitudine, quartiere, via, fascia_oraria'
    res = cindydb.database.select_query(schema_to_view, 'pl', 'nome = %s', (key,))
    edit_pl_form.name.data = key
    edit_pl_form.latitude.data = res[0][0]
    edit_pl_form.longitude.data = res[0][1]
    edit_pl_form.district.data = res[0][2]
    edit_pl_form.street.data = res[0][3]
    edit_pl_form.time_slot.data = res[0][4]
    return edit_pl_form


def get_ppc_tuple(edit_ppc_form, key):
    schema_to_view = 'latitudine, longitudine, quartiere, via, societa, telefono, email, costo_orario'
    res = cindydb.database.select_query(schema_to_view, 'ppc', 'nome = %s', (key,))
    edit_ppc_form.name.data = key
    edit_ppc_form.latitude.data = res[0][0]
    edit_ppc_form.longitude.data = res[0][1]
    edit_ppc_form.district.data = res[0][2]
    edit_ppc_form.street.data = res[0][3]
    edit_ppc_form.company.data = res[0][4]
    edit_ppc_form.tel.data = res[0][5]
    edit_ppc_form.email.data = res[0][6]
    edit_ppc_form.cost.data = res[0][7]
    return edit_ppc_form


def get_pass_tuple(shop_pass_form, key):
    schema_to_view = 'zona_ztl, durata, costo'
    res = cindydb.database.select_query(schema_to_view, 'pass', 'codice = %s', (key,))
    shop_pass_form.cod.data = key
    shop_pass_form.time.data = res[0][1]
    shop_pass_form.cost.data = res[0][2]
    providers = cindydb.database.select_query('ppc.nome', 'ppc', 'char_length(ppc.nome) > 1', None)
    choises = []
    for record in providers:
        choises.append(record + record)
    shop_pass_form.ppc.choices = choises
    auto = cindydb.database.select_query('automobili.targa', 'automobili', 'proprietario = %s', (session.get('cf'),))
    auto_choises = []
    for record in auto:
        auto_choises.append(record + record)
    shop_pass_form.auto.choices = auto_choises
    return shop_pass_form
