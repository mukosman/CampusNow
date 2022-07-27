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
import models

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

@app.route("/profile")
@login_required
def profile():
    #models.user.update
    return render_template("profile.html")

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
            return redirect(url_for("profile"))
        else:
            flash("Password does not match", "error")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for("index"))

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