from wtforms import Form, StringField, PasswordField, validators, DateField, SelectField, RadioField


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

    # email = StringField('Indirizzo Email', validators=[validators.Optional(),
    #                                                    validators.Length(message='Email non valida', min=6, max=35),
    #                                                    validators.Email('Inserisci il tuo indirizzo email')])

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
    name = StringField('Nome PL')
    latitude = StringField('Latitudine', validators=[validators.DataRequired('Inserisci la latitudine')])
    longitude = StringField('Longitudine', validators=[validators.DataRequired('Inserisci la longitudine')])
    district = StringField('Quartiere', validators=[validators.DataRequired('Inserisci il quartiere')])
    street = StringField('Via', validators=[validators.DataRequired('Inserisci la via')])
    time_slot = StringField('Fascia oraria', validators=[validators.DataRequired('Inserisci la fascia oraria')])
