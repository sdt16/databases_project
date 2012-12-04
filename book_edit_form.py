from flask.ext.wtf import Form, TextField, DecimalField, SelectField, DateField, TextAreaField, BooleanField, Optional

class book_edit_form(Form):
    title = TextField("Title")
    imprint = TextField("Imprint")
    eisbn = TextField("eISBN")
    pisbn = TextField("pISBN")
    language = TextField("Language")
    list_price = DecimalField("List Price", places=2, validators=[Optional()])
    currency = SelectField("Currency", choices=[(g,g) for g in ['none', 'USD', 'EUR', 'GBP', 'CAD', 'CNY', 'JPY']])
    release_date = DateField("Release Date")
    publishing_date = DateField("Publishing Date")
    description = TextAreaField("Description")
    bisac = TextField("BISAC")
    bic = TextField("BIC")
    #TODO: Fix this, this needs to be a list.
    territory = SelectField("Countries to sell in", choices=[('none', 'none'), ('US', 'US'), ('GB', 'GB'), ('FR', 'FR'), ('IT', 'IT'), ('CN', 'CN'), ('JP', 'JP'), ('ES', 'ES'), ('IE', 'IE'), ('DE', 'DE')], validators=[Optional()])
    adult = BooleanField("Is this an adult book?")
    edition = TextField("Edition")
    series = SelectField("Series", coerce=int)
    volume = TextField("Volume")
