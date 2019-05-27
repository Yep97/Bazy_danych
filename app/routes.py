from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from app.models import *
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, AppointmentForm
import datetime

now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d")

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Strona główna', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        pacjent = Pacjent.query.filter_by(email=form.username.data).first()
        #lekarz = Lekarz.query.filter_by(email=form.username.data).first()
        #if pacjent is None or not user.check_password(form.password.data) or lekarz is None or not user.check_password(form.password.data):
        if pacjent is None or not pacjent.check_password(form.password.data):
            flash('Niepoprawna nazwa użytkownika lub hasło')
            return redirect(url_for('login'))
        login_user(pacjent, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Zaloguj się', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        pacjent = Pacjent(
            imie=form.imie.data,
            nazwisko=form.nazwisko.data,
            pesel=form.pesel.data,
            data_pw=today,
            data_uro=form.data_uro.data,
            email=form.email.data)
        pacjent.set_password(form.password.data)
        db.session.add(pacjent)
        db.session.commit()
        flash('Gratulacje zostałeś zarejestrowany!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/patients_view', methods=['GET', 'POST'])
def manage_appointments_for_patients():

    appointments = Wizyta.query.all()

    form = AppointmentForm()
    form.placowka_id.choices =[(placowka.id,placowka.adres) for placowka in Placowka.query.all()]
    form.finansowanie_id.choices=[(finansowanie.id,finansowanie.rodzaj) for finansowanie in Finansowanie.query.all()]
    form.lekarz_id.choices = [(lekarz.id, lekarz.nazwisko) for lekarz in Lekarz.query.all()]
    if form.validate_on_submit():
        wizyta = Wizyta(
            id = form.id.data,
            placowka_id = form.placowka_id.data,
            pacjent_id = form.pacjent_id.data,
            lekarz_id = form.lekarz_id.data,
            finansowanie_id = form.finansowanie_id.data,
            termin = form.termin.data,
            typ_wizyty = form.typ_wizyty.data
        )

        db.session.add(wizyta)
        db.session.commit()
        flash('Dodałeś wizytę')
        return redirect(url_for('/patients_view'))


    data = Pacjent.query.all()


    return render_template('patients_view.html', patients=data, form=form, appointments=appointments)


@app.route('/appointment', methods=['GET', 'POST'])
def manage_appointments():
    data = Pacjent.query.all()
    print(data)
    return render_template('appointment.html', patients=data)

@app.route('/authors', methods=['GET'])
def authors():
    return render_template('authors.html')