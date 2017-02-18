import cindydb.database
import datetime


def myconverter(o):
    if isinstance(o, datetime.date):
        return o.__str__()


def get_profile(edit_form, username):
    schema_to_view = 'nome, cognome, data_nascita, tel, email, sesso, residenza'
    res = cindydb.database.select_query(schema_to_view, 'utenti', 'username = %s', username)
    edit_form.firstname_edited.data = res[0][0]
    edit_form.lastname_edited.data = res[0][1]
    edit_form.phonenumber_edited.data = res[0][3]
    edit_form.dob_edited.data = res[0][2]
    edit_form.gender_edited.data = res[0][5]
    edit_form.city_edited.data = res[0][6]
    edit_form.email_edited.data = res[0][4]
    return edit_form


def get_tuple(edit_tuple_form, key):
    schema_to_view = 'nome, cognome, data_nascita, tel, email, sesso, residenza'
    res = cindydb.database.select_query(schema_to_view, 'utenti', 'username = %s', (key,))
    edit_tuple_form.username.data = key
    edit_tuple_form.firstname_edited.data = res[0][0]
    edit_tuple_form.lastname_edited.data = res[0][1]
    edit_tuple_form.phonenumber_edited.data = res[0][3]
    edit_tuple_form.dob_edited.data = res[0][2]
    edit_tuple_form.gender_edited.data = res[0][5]
    edit_tuple_form.city_edited.data = res[0][6]
    edit_tuple_form.email_edited.data = res[0][4]
    return edit_tuple_form

