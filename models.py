from flask_sqlalchemy import SQLAlchemy
from bookmgr import app

db = SQLAlchemy(app)

class VendorCode(db.Model):
	vendor_code = db.Column(db.String, primary_key=True)

	def __init__(vendor_code):
		self.vendor_code = vendor_code


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    vendor_code = db.Column(db.String, db.ForeignKey('vendor_code.vendor_code'), nullable=False)
    vendor_code_relation = db.relationship('VendorCode', backref=db.backref('users', lazy='dynamic'))

    def __init__(username, message, email, password, vendor_code):
        self.username = username
        self.message = message
        self.email = email
        self.password = password
        self.vendor_code = vendor_code

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String)
	imprint = db.Column(db.String)
	eisbn = db.Column(db.String)
	pisbn = db.Column(db.String)
	language = db.Column(db.String)
	list_price = db.Column(db.Integer)
	currency = db.Column(db.Enum(USD, EUR, GBP, CAD, CNY, JPY, name='currencies'))
	release_date = db.Column(db.DateTime)
	publishing_date = db.Column(db.DateTime)
	desciption = db.Column(db.String)
	bisac = db.Column(db.String)
	bic = db.Column(db.String)
	territory = db.Column(db.Enum(US, GB, FR, IT, CN, JP, ES, IE, DE))
	adult = db.Column(db.Boolean)
	edition = db.Column(db.String)
	series_title = db.Column(db.String)
	volume = db.Column(db.String)