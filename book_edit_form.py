from flask.ext.wtf import Form, TextField, DecimalField, SelectField, DateField, \
    TextAreaField, BooleanField, Optional, SelectMultipleField
from wtforms import ValidationError
from isbn import isValid

class book_edit_form(Form):
    title = TextField("Title")
    imprint = TextField("Imprint")
    eisbn = TextField("eISBN", validators=[Optional()])
    pisbn = TextField("pISBN", validators=[Optional()])
    language = TextField("Language")
    list_price = DecimalField("List Price", places=2, validators=[Optional()])
    currency = SelectField("Currency", choices=[(g,g) for g in ['none', 'USD', 'EUR', 'GBP', 'CAD', 'CNY', 'JPY']])
    release_date = DateField("Release Date", validators=[Optional()], format='%m/%d/%Y')
    publishing_date = DateField("Publishing Date", validators=[Optional()], format='%m/%d/%Y')
    description = TextAreaField("Description")
    bisac = TextField("BISAC")
    bic = TextField("BIC")
    #TODO: Fix this, this needs to be a list.
    territory = SelectField("Countries to sell in", choices=[('none', 'none'), ('US', 'US'), ('GB', 'GB'), ('FR', 'FR'), ('IT', 'IT'), ('CN', 'CN'), ('JP', 'JP'), ('ES', 'ES'), ('IE', 'IE'), ('DE', 'DE')], validators=[Optional()])
    adult = BooleanField("Is this an adult book?")
    edition = TextField("Edition")
    series = SelectField("Series", coerce=int)
    volume = TextField("Volume")
    authors = SelectMultipleField("Authors", coerce=int)
    editors = SelectMultipleField("Editors", coerce=int)
    illustrators = SelectMultipleField("Illustrators", coerce=int)
    contributors =  SelectMultipleField("Contributors", coerce=int)
    translators = SelectMultipleField("Translators", coerce=int)

    def validate_publishing_date(self, field):
        if field.data > self.release_date.data:
            raise ValidationError("The publishing date must be before or equal to the release date.")

    def is_isbn_valid(self, isbn):
        if not isValid(isbn):
            raise ValidationError("The ISBN entered is not valid.")

    def validate_eisbn(self, field):
        self.is_isbn_valid(field.data)

    def validate_pisbn(self, field):
        self.is_isbn_valid(field.data)


