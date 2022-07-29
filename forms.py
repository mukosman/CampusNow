from choices import RACES_IN_CHOICES,GENDER_CHOICES,YEAR_IN_SCHOOL_CHOICES
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextField, TextAreaField, IntegerField,SelectField,DecimalField
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

class ProfileForm(Form):
    name = StringField("Name", validators=[DataRequired()])
    address = IntegerField("Zipcode",validators=[DataRequired()])
    phone = IntegerField("Phone")
    race = SelectField("Race",choices = RACES_IN_CHOICES)
    gender = SelectField("Gender", choices = GENDER_CHOICES)

    highschool =StringField("Name",validators = [DataRequired()], id='highschool_input')
    gpa = DecimalField("GPA",validators = [DataRequired()])
    standings = SelectField("Standing", choices = YEAR_IN_SCHOOL_CHOICES)
    grad_year = IntegerField("Grad Year",validators = [DataRequired()])
    sat_reading_writing = IntegerField("SAT Reading and Writing",validators = [DataRequired()])
    sat_math = IntegerField("SAT Math",validators = [DataRequired()])
    act = IntegerField("ACT Composite",validators = [DataRequired()])

    preferred_major = StringField("Preferred Major", validators=[DataRequired()])
    alternate_major = StringField("Alternate Major", validators=[DataRequired()])
    sports = StringField("Sport", validators=[DataRequired()])
    religion = StringField("Religion", validators=[DataRequired()])