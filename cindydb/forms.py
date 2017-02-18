from wtforms import Form, StringField, PasswordField, validators, DateField, SelectField, RadioField


class Registration(Form):
    firstname = StringField('Nome', validators=[validators.DataRequired('Inserisci il tuo nome')])

    lastname = StringField('Cognome', validators=[validators.DataRequired('Inserisci il tuo cognome')])

    phonenumber = StringField('Numero di telefono')

    dob = DateField('Data di nascita', validators=[validators.Optional()])

    gender = RadioField('Sesso', default='uomo', choices=[('uomo', 'Uomo'),
                                                           ('donna', 'Donna')],
                         validators=[validators.Optional()])

    city = StringField('Residenza', validators=[validators.Optional()])

    username = StringField('Username', validators=[validators.DataRequired('Inserisci il tuo username'),
                                                   validators.Length(message='Username non valido: lunghezza minima 4.',
                                                                     min=4, max=25)])

    email = StringField('Indirizzo Email', validators=[validators.Optional(),
                                                       validators.Length(message='Email non valida', min=6, max=35),
                                                       validators.Email('Inserisci il tuo indirizzo email')])

    password = PasswordField('Password', validators=[validators.DataRequired('Password obbligatoria'),
                                                     validators.Length(message='Password troppo corta: lunghezza minima 4.',
                                                                       min=4, max=25),
                                                     validators.EqualTo('confirm', message='Le passwords devono corrispondere!')])
    confirm = PasswordField('Conferma password')


class Edit(Form):
    firstname_edited = StringField('Nome', validators=[validators.DataRequired('Inserisci il tuo nome')])

    lastname_edited = StringField('Cognome', validators=[validators.DataRequired('Inserisci il tuo cognome')])

    phonenumber_edited = StringField('Numero di telefono')

    dob_edited = DateField('Data di nascita', validators=[validators.Optional()])

    gender_edited = RadioField('Sesso', default='uomo', choices=[('uomo', 'Uomo'),
                                                           ('donna', 'Donna')],
                         validators=[validators.Optional()])

    city_edited = StringField('Residenza', validators=[validators.Optional()])

    email_edited = StringField('Indirizzo Email', validators=[validators.Optional(),
                                                       validators.Length(message='Email non valida', min=6, max=35),
                                                       validators.Email('Inserisci il tuo indirizzo email')])


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

