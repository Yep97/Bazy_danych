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
from app.forms import *
import datetime

now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d")

@app.route('/')
def start_page():
    return render_template('start_page.html')

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
            email=form.email.data,
            isLekarz = 0,
            isRecepcja = 0)
        pacjent.set_password(form.password.data)
        db.session.add(pacjent)
        db.session.commit()
        flash('Gratulacje zostałeś zarejestrowany!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/reception_view', methods=['GET', 'POST'])
def manage_appointments_for_reception():
    if current_user.isRecepcja == 0:
        flash("Nie jesteś z recepcji, więc nie możesz tutaj wejść!")
        manage_appointments()
    form = CreateAppointmentForm()
    form.placowka_id.choices =[(placowka.id, placowka.adres) for placowka in Placowka.query.all()]
    form.finansowanie_id.choices=[(finansowanie.id,finansowanie.rodzaj) for finansowanie in Finansowanie.query.all()]
    form.lekarz_id.choices = [(lekarz.id, lekarz.nazwisko) for lekarz in Lekarz.query.all()]
    if form.validate_on_submit():
        wizyta = Wizyta(
            id = form.id.data,
            placowka_id =form.placowka_id.data,
            pacjent_id = form.pacjent_id.data,
            lekarz_id = form.lekarz_id.data,
            finansowanie_id = form.finansowanie_id.data,
            termin = form.termin.data,
            typ_wizyty = form.typ_wizyty.data
        )
        print(wizyta)
        db.session.add(wizyta)
        db.session.commit()
        flash('Dodałeś wizytę')
    else:
        print(form.lekarz_id.data)
        print(form.errors)

    data = Pacjent.query.all()
    appointments = Wizyta.query.all()
    return render_template('reception_view.html', patients=data, form=form, appointments=appointments)

@app.route('/patients_view', methods=['GET', 'POST'])
def manage_appointments_for_patients():
    form = RegisterForAppointmentForm()
    appointments2 = Wizyta.query.filter_by(pacjent_id=current_user.id)
    choicesToRegister = Wizyta.query.filter_by(pacjent_id=0).all()
    appointments2 = Wizyta.query.filter_by(pacjent_id=current_user.id)
    form.id.choices = [(appointment.id, appointment.id)for appointment in choicesToRegister]

    if form.validate_on_submit():
        chosenAppointment = Wizyta.query.filter_by(id=form.id.data).first()
        chosenAppointment.pacjent_id = current_user.id
        db.session.commit()
        manage_appointments_for_patients()

    return render_template('patients_view.html', form=form,
                           appointmentsToChoose=choicesToRegister,
                           appointmentsThisPatientRegistrated=appointments2)

@app.route('/appointment', methods=['GET', 'POST'])
def manage_appointments():
    data = Pacjent.query.all()
    return render_template('appointment.html', patients=data)

@app.route('/docs_view', methods=['GET', 'POST'])
def manage_appointments_for_docs():
    if current_user.isLekarz == 0:
        flash("Nie możesz tutaj wejść, nie jesteś lekarzem!")
        manage_appointments()

    form = SelectDoctorToShow()
    form.id.choices = [(lekarz.id, lekarz.nazwisko) for lekarz in Lekarz.query.all()]
    if form.validate_on_submit():
        thisDoctorAppointments = Wizyta.query.filter_by(lekarz_id=form.id.data)
        return render_template('docs_view.html',form=form, appointments=thisDoctorAppointments)
    else:
        flash(form.errors)

    return render_template('docs_view.html', form=form, appointments=[])

@app.route('/authors', methods=['GET'])
def authors():
    return render_template('authors.html')
