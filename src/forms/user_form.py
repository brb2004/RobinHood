from wtforms import validators, Form, StringField, PasswordField

class UserForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
    ])
    username = StringField('Username', [validators.Length(min=4, max=25)])