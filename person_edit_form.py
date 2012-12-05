from flask.ext.wtf import Form, TextField, DateField, Optional

class person_form(Form):
    first_name = TextField("First name")
    last_name = TextField("Last name")
    birthday = DateField("Birthday", validators=[Optional()], format="%m/%d/%Y")
