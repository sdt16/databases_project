from flask_sqlalchemy import SQLAlchemy
from flask import Flask

#configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
SQLALCHEMY_DATABASE_URI = 'postgresql://devo:test@localhost:5432/bookmgr_test'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('BOOKMGR_SETTINGS', silent=True)

db = SQLAlchemy(app)

class VendorCode(db.Model):
    vendor_code = db.Column(db.String, primary_key=True)

    def __init__(self, vendor_code):
        self.vendor_code = vendor_code


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    vendor_code = db.Column(db.String, db.ForeignKey('vendor_code.vendor_code'), nullable=False)
    #vendor_code_relation = db.relationship('VendorCode', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username, message, email, password, vendor_code):
        self.username = username
        self.message = message
        self.email = email
        self.password = password
        self.vendor_code = vendor_code

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_code = db.Column(db.String, db.ForeignKey('vendor_code.vendor_code'), nullable=False)
    #vendor_code_relation = db.relationship('VendorCode', backref=db.backref('users', lazy='dynamic'))
    title = db.Column(db.String)
    imprint = db.Column(db.String)
    eisbn = db.Column(db.String)
    pisbn = db.Column(db.String)
    language = db.Column(db.String)
    list_price = db.Column(db.Numeric)
    currency = db.Column(db.Enum('USD', 'EUR', 'GBP', 'CAD', 'CNY', 'JPY', 'none', name='currencies'))
    release_date = db.Column(db.DateTime)
    publishing_date = db.Column(db.DateTime)
    description = db.Column(db.String)
    bisac = db.Column(db.String)
    bic = db.Column(db.String)
    territory = db.Column(db.Enum('US', 'GB', 'FR', 'IT', 'CN', 'JP', 'ES', 'IE', 'DE', 'none', name='country_codes'))
    adult = db.Column(db.Boolean)
    edition = db.Column(db.String)
    series = db.Column(db.Integer, db.ForeignKey('series.id'))
    volume = db.Column(db.String)


    def __init__(self, vendor_code=None, title=None, imprint=None, eisbn=None, pisbn=None, language=None,
                 list_price=None, currency=None, release_date=None, publishing_date=None, desciption=None,
                 bisac=None, bic=None, territory=None, adult=None, edition=None, series=None, volume=None):
        self.vendor_code = vendor_code
        self.title = title
        self.imprint = imprint
        self.eisbn = eisbn
        self.pisbn = pisbn
        self.language = language
        self.list_price = list_price
        self.currency = currency
        self.release_date = release_date
        self.publishing_date = publishing_date
        self.description = desciption
        self.bisac = bisac
        self.bic = bic
        self.territory = territory
        self.adult = adult
        self.edition = edition
        self.series = series
        self.volume = volume


class Authors(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)

    def __init__(self, book_id, person_id):
        self.book_id = book_id
        self.person_id = person_id

class Editors(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)

    def __init__(self, book_id, person_id):
        self.book_id = book_id
        self.person_id = person_id

class Illustrators(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)

    def __init__(self, book_id, person_id):
        self.book_id = book_id
        self.person_id = person_id

class Contributors(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)

    def __init__(self, book_id, person_id):
        self.book_id = book_id
        self.person_id = person_id


class Translators(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)

    def __init__(self, book_id, person_id):
        self.book_id = book_id
        self.person_id = person_id

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable = False)
    birthday = db.Column(db.DateTime)

    def __init__(self, first_name, last_name, birthday):
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday

class Series(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable = False)
    begin_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    def __init__(self, title, begin_date, end_date):
        self.title = title
        self.begin_date = begin_date
        self.end_date = end_date