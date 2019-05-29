from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, DateTimeField, TimeField
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

class CreateAppointmentForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()])
    placowka_id = SelectField('Placowka ', choices=[], coerce=int)
    pacjent_id = StringField('ID pacjenta', validators=[DataRequired()] )
    lekarz_id = SelectField('Lekarz', choices=[], validators=[DataRequired()], coerce=int)
    finansowanie_id = SelectField('Finansowanie',choices=[], validators=[DataRequired()], coerce=int)
    termin = DateTimeField('Termin(w formacie %Y-%m-%d %H:%M:%S)', validators=[DataRequired()])
    typ_wizyty = StringField('Typ wizyty', validators=[DataRequired()])
    submit = SubmitField('Dodaj wizytę')

class RegisterForAppointmentForm(FlaskForm):
    id = SelectField('Na którą wizytę chcesz się zapisać',coerce=int,choices=[] ,validators=[DataRequired()])
    submit = SubmitField('Zapisz mnie')

class SelectDoctorToShow(FlaskForm):
    id = SelectField('Którego doktora chcesz zobaczyć', coerce=int, choices=[], validators=[DataRequired()])
    submit = SubmitField('Pokaż jego wizyty')