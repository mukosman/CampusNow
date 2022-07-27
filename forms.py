from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextField, TextAreaField
from wtforms.validators import (
    DataRequired,
    ValidationError,
    Email,
    Length,
    EqualTo,
    Regexp,
)
from models import user

def email_exists(form, field):
    if user.select().where(user.email == field.data).exists():
        raise ValidationError("Account with that email already exists")

class RegisterForm(Form):
    email = StringField("Email", validators=[DataRequired(), Email(), email_exists])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo("password2", message="Passwords must match"),
        ],
    )
    password2 = PasswordField("Confirm Password", validators=[DataRequired()])

class LoginForm(Form):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])