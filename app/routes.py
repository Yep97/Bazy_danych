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
from app.forms import RegistrationForm
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

@app.route('/appointment', methods=['GET', 'POST'])
def manage_appointments():
    data = Pacjent.query.all()
    print(data)
    return render_template('appointment.html', patients=data)

@app.route('/authors', methods=['GET'])
def authors():
    return render_template('authors.html')