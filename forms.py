from wtforms import Form, StringField, TextAreaField, PasswordField
from wtforms.validators import Email, DataRequired, Length, EqualTo

class RegisterForm(Form):
    name = StringField('Name', [Length(min=1, max=50)])
    username = StringField('Username', [Length(min=4, max=25), DataRequired()])
    email = StringField('Email', [Length(min=6, max=50), Email(), DataRequired()])
    password = PasswordField('Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password', [DataRequired()])


class LoginForm(Form):
    username = StringField('Username', [Length(min=4, max=25), DataRequired()])
    password = PasswordField('Password', [DataRequired(),])
    