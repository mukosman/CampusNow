from flask import Flask, render_template, request,g,url_for,flash,redirect
import requests, stripe
import forms
from flask_bcrypt import Bcrypt, check_password_hash
from flask_login import (
    LoginManager,
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from flask import request 
import models
from choices import getData
import favicon
from pandas import read_excel 
import os

HOST = '0.0.0.0'
DEBUG = True

app = Flask(__name__)
app.config["SECRET_KEY"] = '02fa4a01a5320cbbdfaaba368a71b043'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(userid):
    try:
        return models.user.get(models.user.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """connect to database before connecting"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response

@app.route("/",)
def index():
    return render_template("index.html")

@app.route("/profile",methods=("GET", "POST"))
@login_required
def profile():
    highschools = getData()
    form = forms.ProfileForm()
    if form.validate_on_submit():
        models.user.update_user(
            email = current_user.email,
            name = form.name.data,
            address = form.address.data,
            phone = form.phone.data,
            gender = form.gender.data,
            race = form.race.data,
            highschool = form.highschool.data,
            standings = form.standings.data,
            gpa = form.gpa.data,
            grad_year = form.grad_year.data,
            sat_math = form.sat_math.data,
            sat_reading_writing = form.sat_reading_writing.data,
            act = form.act.data,
            preferred_major = form.preferred_major.data,
            alternate_major = form.alternate_major.data,
            sports = form.sports.data,
            religion = form.religion.data)
        
        return redirect(url_for("home"))
    return render_template("profile.html",form = form, highschools = highschools)

@app.route("/home")
@login_required
def home():
    #will handle the search function and showcase recommendations 
    return render_template("home.html")

@app.route("/registration",methods=("GET", "POST"))
def registration():
    form = forms.RegisterForm()
    if form.validate_on_submit():

        flash("Yay, you registered!", "success")

        models.user.create_user(email=form.email.data, password=form.password.data)

        return redirect(url_for("login"))

    return render_template("registration.html",form = form)


@app.route("/login", methods=("GET", "POST"))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.user.get(models.user.email == form.email.data)
        except models.DoesNotExist:
            flash("Email is incompatible", "error")

        if check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("You are logged in", "success")
            return redirect(url_for("home"))
        else:
            flash("Password does not match", "error")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for("index"))




@app.route("/searching",methods=["POST"])
def searching():
    apiurl = "https://api.data.gov/ed/collegescorecard/v1/schools.json"
    params={}
    params["api_key"]=os.environ.get('api_key')
    svars=getsearchvars()
    for x in svars:
        something=eval(x[3])
        if something:
            params[str(x[1])]=something
    print(params)
    response = requests.get(f"{apiurl}", params=params)
    response=response.json()
    print(response)
    return response

def getsearchvars():    
    df=read_excel("CollegeScorecardDataDictionary.xlsx",sheet_name="Institution_Data_Dictionary",usecols="L")
    searchvars=[]
    for x in range(3251):
        searchvar=df.iloc[x][0]
        if str(searchvar)!="nan":
            searchvar=df.iloc[x][0]
            searchvar=searchvar.split(",")
            searchvar=tuple(searchvar)
            searchvars.append(searchvar)
    return searchvars

@app.route("/dummysearch",methods=["GET"])
def dummy():
    return render_template("dummysearch.html")

def getfavicon(url):
    icons = favicon.get(url)
    icon = icons[0]
    response = requests.get(icon.url, stream=True)
    with open('D:/School/CampusNow/tmp/python-favicon.{}'.format(icon.format), 'wb') as image:
        return response
if __name__== '__main__':
    models.initialize()
    try:
        models.user.create_user(
            email="stisselin216@gmail.com",
            password="123",
        )
    except ValueError:
        pass
    app.run(host = HOST,debug = DEBUG) 