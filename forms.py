from choices import RACES_IN_CHOICES,GENDER_CHOICES,YEAR_IN_SCHOOL_CHOICES,STATE_IN_CHOICES,RELIGONS,SIZE_TYPE_CHOICES,SCHOOL_TYPE_CHOICES,ACCEPTANCE_IN_CHOICES,DEGREES
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, IntegerField,SelectField,DecimalField
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

class RegisterForm(FlaskForm):
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

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class ProfileForm(FlaskForm):
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
    religion = SelectField("Religion", validators=[DataRequired()],choices = RELIGONS)

class SearchForm(FlaskForm):
    search_query = StringField("Search",validators=[DataRequired()],render_kw={"placeholder": "Search.."} )

class AdvancedSearchForm(FlaskForm):
    state = SelectField("State",choices = STATE_IN_CHOICES,validators=[DataRequired()])
    school_type = SelectField("School Type",validators=[DataRequired()],choices = SCHOOL_TYPE_CHOICES)
    highest_degree = SelectField("Highest Degree", validators=[DataRequired()],choices = DEGREES)
    #specialty = SelectField("Specialty School", validators = [DataRequired()])
    #affiliated_religion = ooleanField("Affiliated Religion",validators=[DataRequired()])
    campus_size = SelectField("Campus Size",validators=[DataRequired()],choices = SIZE_TYPE_CHOICES)
    #campus_housing = BooleanField("On-Campus Housing?",validators=[DataRequired()])
    #diversity = SelectField("Diversity Preference", validators = [DataRequired()])
    acceptance_rate = SelectField('Acceptance Rate',validators=[DataRequired()],choices= ACCEPTANCE_IN_CHOICES)
    #annual_cost = SelectField('Annual Cost', validators = [DataRequired()])
    close_to_score = BooleanField('Close to my score')

    


