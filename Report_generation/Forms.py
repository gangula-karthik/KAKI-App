from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, DateField

class CreateUserForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    description = TextAreaField('Description', [validators.Optional()])
    date_posted = DateField('Date posted', [validators.DataRequired()])
    event_date = DateField('Event Date', [validators.DataRequired()])
