from wtforms import Form, StringField, PasswordField, validators, DateField, SelectField, RadioField
import datetime
from time import gmtime, strftime


class Registration(Form):
    firstname = StringField('Nome', validators=[validators.DataRequired('Inserisci il tuo nome')])

    lastname = StringField('Cognome', validators=[validators.DataRequired('Inserisci il tuo cognome')])

    number = StringField('Numero di patente', validators=[validators.DataRequired('Inserisci il tuo numero di patente')])

    cf = StringField('Codice fiscale', validators=[validators.DataRequired('Inserisci il tuo codice fiscale')])

    dob = DateField('Data di nascita', validators=[validators.DataRequired('Inserisci la tua data di nascita [%Y-%m-%d]')])

    gender = RadioField('Sesso', default='uomo', choices=[('uomo', 'Uomo'), ('donna', 'Donna')],
                        validators=[validators.Optional()])

    type = RadioField('Tipo di utente', default='ua', choices=[('up', 'Utente premium'),
                                                               ('ua', 'Utente abbonato')])

    username = StringField('Username', validators=[validators.DataRequired('Inserisci il tuo username'),
                                                   validators.Length(message='Username non valido: lunghezza minima 4.',
                                                                     min=4, max=25)])

    password = PasswordField('Password', validators=[validators.DataRequired('Password obbligatoria'),
                                                     validators.Length(message='Password troppo corta: lunghezza minima 4.',
                                                                       min=4, max=25),
                                                     validators.EqualTo('confirm', message='Le passwords devono corrispondere!')])
    confirm = PasswordField('Conferma password')


class Edit(Form):
    firstname_edited = StringField('Nome', validators=[validators.DataRequired('Inserisci il tuo nome')])

    lastname_edited = StringField('Cognome', validators=[validators.DataRequired('Inserisci il tuo cognome')])

    number_edited = StringField('Numero di patente', validators=[validators.DataRequired('Inserisci il tuo numero di patente')])

    dob_edited = DateField('Data di nascita', validators=[validators.DataRequired('Inserisci la tua data di nascita [%Y-%m-%d]')])

    gender_edited = RadioField('Sesso', default='uomo', choices=[('uomo', 'Uomo'),
                                                           ('donna', 'Donna')],
                               validators=[validators.Optional()])

    type_edited = RadioField('Tipo di utente', default='ua', choices=[('up', 'Utente premium'),
                                                                      ('ua', 'Utente abbonato')])


class Login(Form):
    login_user = StringField('Username', [validators.DataRequired('Inserisci il tuo username')])
    login_pass = PasswordField('Password', [validators.DataRequired('Inserisci la tua password')])


class ChangePassword(Form):
    oldpassword = PasswordField('Password attuale', validators=[validators.DataRequired('Inserisci la password attuale')])
    newpassword = PasswordField('Nuova password', validators=[validators.DataRequired('Inserisci una nuova password'),
                                                     validators.Length(
                                                         message='Password troppo corta: lunghezza minima 4.',
                                                         min=4, max=25),
                                                     validators.EqualTo('confirm',
                                                                        message='Le passwords devono corrispondere!')])
    confirm = PasswordField('Conferma password')


class EditTuple(Form):
    cf = StringField('Codice fiscale')
    username = StringField('Username')
    firstname_edited = StringField('Nome', validators=[validators.DataRequired('Inserisci il tuo nome')])

    lastname_edited = StringField('Cognome', validators=[validators.DataRequired('Inserisci il tuo cognome')])

    number_edited = StringField('Numero di patente',
                                validators=[validators.DataRequired('Inserisci il tuo numero di patente')])

    dob_edited = DateField('Data di nascita',
                           validators=[validators.DataRequired('Inserisci la tua data di nascita [%Y-%m-%d]')])

    gender_edited = RadioField('Sesso', default='uomo', choices=[('uomo', 'Uomo'),
                                                           ('donna', 'Donna')],
                         validators=[validators.Optional()])

    type_edited = RadioField('Tipo di utente', default='ua', choices=[('up', 'Utente premium'),
                                                                      ('ua', 'Utente abbonato')])


class EditPL(Form):
    name = StringField('Nome PL', validators=[validators.DataRequired('Inserisci il nome del PL')])
    latitude = StringField('Latitudine', validators=[validators.DataRequired('Inserisci la latitudine')])
    longitude = StringField('Longitudine', validators=[validators.DataRequired('Inserisci la longitudine')])
    district = StringField('Quartiere', validators=[validators.DataRequired('Inserisci il quartiere'),
                                                    validators.Length(
                                                        message='Quartiere non valido [lunghezza massima 20]', max=20)])
    street = StringField('Indirizzo', validators=[validators.DataRequired('Inserisci l\'indirizzo'),
                                            validators.Length(message='Indirizzo non valido [lunghezza massima 50]',
                                                              max=50)])
    time_slot = StringField('Fascia oraria', validators=[validators.DataRequired('Inserisci la fascia oraria')])


class EditPPC(Form):
    name = StringField('Nome PPC', validators=[validators.DataRequired('Inserisci il nome del PPC')])
    latitude = StringField('Latitudine', validators=[validators.DataRequired('Inserisci la latitudine')])
    longitude = StringField('Longitudine', validators=[validators.DataRequired('Inserisci la longitudine')])
    district = StringField('Quartiere', validators=[validators.DataRequired('Inserisci il quartiere'),
                                                    validators.Length(
                                                        message='Quartiere non valido [lunghezza massima 20]', max=20)])
    street = StringField('Indirizzo', validators=[validators.DataRequired('Inserisci l\'indirizzo'),
                                            validators.Length(message='Indirizzo non valido [lunghezza massima 50]',
                                                              max=50)])
    company = StringField('Societa\'', validators=[validators.DataRequired('Inserisci la societa\'')])
    tel = StringField('Telefono', validators=[validators.DataRequired('Inserisci il numero di telefono'),
                                              validators.Length(message='Email non valida', max=15)])
    email = StringField('Indirizzo Email', validators=[validators.DataRequired('Inserisci l\'indirizzo Email'),
                                                       validators.Length(message='Email non valida', min=6, max=35),
                                                       validators.Email('Inserisci l\'indirizzo email della societa\'')])
    cost = StringField('Costo orario unitario', default='0.5', validators=[validators.Optional()])


class ShopPass(Form):
    cod = StringField('Codice PASS')
    time = StringField('Durata PASS [mesi]')
    cost = StringField('Costo PASS [euro]')
    ppc = SelectField('PPC',
                      validators=[validators.DataRequired('Non sono disponibili PPC')])
    auto = SelectField('Automobile',
                       validators=[validators.DataRequired('Non hai registrato automobili')])
    date = DateField('Data di rilascio', default=datetime.datetime.now().date())


class NewAuto(Form):
    targa = StringField('Targa', validators=[validators.DataRequired('Inserisci la targa della tua auto')])
    modello = StringField('Modello auto', validators=[validators.DataRequired('Inserisci il modello della tua auto')])
    marca = StringField('Marca auto', validators=[validators.DataRequired('Inserisci la marca della tua auto')])
    lung = StringField('Lunghezza auto', validators=[validators.Optional()])
    larg = StringField('Larghezza auto', validators=[validators.Optional()])


class Booking(Form):

    auto = SelectField('Automobile',
                       validators=[validators.DataRequired('Non hai registrato automobili')])
    data_inizio = StringField('Data di inzio sosta', default=datetime.datetime.today().replace(microsecond=0),
                            validators=[validators.DataRequired('Inserisci la data di inizio sosta')])
    data_fine = StringField('Data di fine sosta [%Y-%m-%d %H:%M:%S]', validators=[validators.DataRequired('Inserisci la'
                                                                                                        ' data di fine '
                                                                                                        'sosta')])


class NewPPC(Form):
    name = StringField('Nome PPC', validators=[validators.DataRequired('Inserisci il nome del PPC')])
    latitude = StringField('Latitudine', validators=[validators.DataRequired('Inserisci la latitudine')])
    longitude = StringField('Longitudine', validators=[validators.DataRequired('Inserisci la longitudine')])
    district = StringField('Quartiere', validators=[validators.DataRequired('Inserisci il quartiere'),
                                                    validators.Length(
                                                        message='Quartiere non valido [lunghezza massima 20]', max=20)])
    street = StringField('Indirizzo', validators=[validators.DataRequired('Inserisci l\'indirizzo'),
                                            validators.Length(message='Indirizzo non valido [lunghezza massima 50]',
                                                              max=50)])
    company = StringField('Societa\'', validators=[validators.DataRequired('Inserisci la societa\'')])
    tel = StringField('Telefono', validators=[validators.DataRequired('Inserisci il numero di telefono'),
                                              validators.Length(message='Email non valida', max=15)])
    email = StringField('Indirizzo Email', validators=[validators.DataRequired('Inserisci l\'indirizzo Email'),
                                                       validators.Length(message='Email non valida', min=6, max=35),
                                                       validators.Email('Inserisci l\'indirizzo email della societa\'')])
    cost = StringField('Costo orario unitario', default='0.5', validators=[validators.Optional()])

    number = StringField('Numero di posti auto', validators=[validators.Optional()])
    sensor = SelectField('Sensore', validators=[validators.Optional()])
    lung = StringField('Lunghezza posti auto', validators=[validators.Optional()])
    larg = StringField('Larghezza posti auto', validators=[validators.Optional()])

