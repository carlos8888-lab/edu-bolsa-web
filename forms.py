from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=10, max=128)])
    password2 = PasswordField("Repite contraseña", validators=[DataRequired(), EqualTo("password")])

class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField("Contraseña", validators=[DataRequired()])
