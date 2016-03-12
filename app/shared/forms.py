from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired, EqualTo


class LoginForm(Form):
	username = TextField('Username', [InputRequired()])
	password = PasswordField('Password', [InputRequired()])