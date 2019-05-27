from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Pacjent

class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember_me = BooleanField('Pamiętaj mnie')
    submit = SubmitField('Zaloguj się')

class RegistrationForm(FlaskForm):
    imie = StringField('Imie', validators=[DataRequired()])
    nazwisko = StringField('Nazwisko', validators=[DataRequired()])
    pesel = StringField('PESEL', validators=[DataRequired()])
    data_uro = StringField('Data urodzenia', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        pacjent = Pacjent.query.filter_by(email=email.data).first()
        if pacjent is not None:
            raise ValidationError('Podany adres email został już użyty')

class AppointmentForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    placowka_id = SelectField('placowka_id', choices=[])
    pacjent_id = StringField('ID pacjenta', validators=[DataRequired()])
    lekarz_id = SelectField('ID lekarza', choices=[], validators=[DataRequired()])
    finansowanie_id = SelectField('Finansowanie',choices=[], validators=[DataRequired()])
    termin = StringField('Termin', validators=[DataRequired()])
    typ_wizyty = StringField('Termin', validators=[DataRequired()])
    submit = SubmitField('Dodaj wizytę')
