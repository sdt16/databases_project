from flask.ext.wtf import Form, TextField, DateField, Optional

class edit_series(Form):
    title = TextField("Series title")
    begin_date = DateField("Begin date", validators=[Optional()], format='%m/%d/%Y')
    end_date = DateField("End date", validators=[Optional()], format='%m/%d/%Y')

