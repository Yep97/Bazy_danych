from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_pacjent(id):
    return Pacjent.query.get(int(id))
def load_lekarz(id):
    return Lekarz.query.get(int(id))

class Pacjent(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    imie = db.Column(db.String(255), index=True, nullable=False)
    nazwisko = db.Column(db.String(255), index=True, nullable=False)
    pesel = db.Column(db.Integer, index=True, nullable=False, unique=True)
    data_uro = db.Column(db.String(255), index=True, nullable=False)
    data_pw = db.Column(db.String(255), index=True, nullable=False)
    email = db.Column(db.String(255), index=True, nullable=False, unique=True)
    haslo = db.Column(db.String(128))
    isLekarz = db.Column(db.Boolean(), index=True, nullable=False)
    isRecepcja = db.Column(db.Boolean(), index=True, nullable=False)

    user_id = db.relationship('Wizyta', backref='Wizyta Pacjenta', lazy='dynamic')

    def set_password(self, password):
        self.haslo = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.haslo, password)

    def __repr__(self):
        return '<Pacjent: {} {}>'.format(self.imie, self.nazwisko)   

class Lekarz(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    imie = db.Column(db.String(255), index=True, nullable=False)
    nazwisko = db.Column(db.String(255), index=True, nullable=False)
    specjalizacja = db.Column(db.String(255), index=True, nullable=False)
    cena = db.Column(db.Float(4), index=True, nullable=False)
    godzina_str = db.Column(db.String(255), index=True, nullable=False)
    godzina_kon = db.Column(db.String(255), index=True, nullable=False)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    haslo = db.Column(db.String(128))

    doc_id = db.relationship('Wizyta', backref='Wizyta Lekarza', lazy='dynamic')

    def set_password(self, password):
        self.haslo = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.haslo, password)

    def __repr__(self):
        return '<Lekarz: {} {} {}>'.format(self.imie, self.nazwisko, self.specjalizacja)   

class Finansowanie(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    rodzaj = db.Column(db.String(255), index=True, nullable=False)

    fin_id = db.relationship('Wizyta', backref='Dofinansowanie Wizyty', lazy='dynamic')

    def __repr__(self):
        return '<Finansowanie: {}>'.format(self.rodzaj)  

class Placowka(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    adres = db.Column(db.String(255), index=True, nullable=False, unique=True)
    godzina_otw = db.Column(db.String(255), index=True, nullable=False)
    godzina_zam = db.Column(db.String(255), index=True, nullable=False)

    place_id = db.relationship('Wizyta', backref='Placówka Wizyty', lazy='dynamic')

    def __repr__(self):
        return '<Placowka: {} od {} do {}>'.format(self.adres, self. godzina_otw, self.godzina_zam)  

class Wizyta(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    placowka_id = db.Column(db.Integer, db.ForeignKey('placowka.id'), nullable=False)
    pacjent_id = db.Column(db.Integer, db.ForeignKey('pacjent.id'), nullable=False)
    lekarz_id = db.Column(db.Integer, db.ForeignKey('lekarz.id'), nullable=False)
    finansowanie_id = db.Column(db.Integer, db.ForeignKey('finansowanie.id'), nullable=False)
    termin = db.Column(db.String(255), index=True, nullable=False)
    typ_wizyty = db.Column(db.String(255), index=True, nullable=False)

    def __repr__(self):
        return '<Wizyta: {} {} {} {} {} {}>'.format(self.placowka_id, self. pacjent_id, self.lekarz_id, self.finansowanie_id, self.termin, self.typ_wizyty)
