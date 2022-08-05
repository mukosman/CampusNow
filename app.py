from inspect import Attribute
import re
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
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
 
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


@app.route("/graphimage.html")
def show():
    return render_template("graphimage.html")


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

@app.route("/graphoptions", methods=["GET"])
def makegraphoptions():
    return render_template("graphoptions.html")

@app.route("/displaygraph",methods=["POST"])
def displaygraph():
    print(request.form)
    for x in request.form:
        category=(x)
    name=(request.form.get((x)))
    print("category is a "+category+" and attribute is a "+name)
    colleges=[]
    colleges.append("002115")
    colleges.append("001315")
    colleges.append("002128")
    colleges=getinfo(colleges)
    data=getgraphdata(colleges,category,name)
    #print(category)
    #print(attribute)
    #print(data)
    #print(data)
    color=getgraphcolors(colleges)
    if (savegraph(data[0],data[1],color)==0):
        return render_template("graphimage.html")
    else:
        return "<h1>This failed fam. </h1>"




@app.route("/graphshow", methods=["GET"])
def showgraph():
    colleges=[]
    colleges.append("002115")
    colleges.append("001315")
    colleges.append("002128")
    colleges=getinfo(colleges)
    data=getgraphdata(colleges,"student","size")
    color=getgraphcolors(colleges)
    if (savegraph(data[0],data[1],color)==0):
        return '''<img src={{ url_for('tmp', filename = 'my_plot.png') }}"/>'''
    else:
        return "<h1>This failed fam. </h1>"

@app.route("/dummysearch", methods=["GET"])
def dummy():
    return render_template("dummysearch.html")
    

@app.route("/searching",methods=["POST"])
def searching():
    apiurl = "https://api.data.gov/ed/collegescorecard/v1/schools.json"
    params={}
    params["api_key"]=os.environ.get('api_key')
    svars=getsearchvars()
    for x in svars:
        something=eval(x[3])
        if something:
            try:
                if(something[0:2]=="NOT"):
                    x[1]=str(x[1])+"__not"
                    params[x[1]]=something[3:]
                elif(something[0:4]=="RANGE"):
                    x[1]=str(x[1])+"__range"
                    params[x[1]]=something[5:]                    
            except:
                pass
            params[str(x[1])]=something
    response = requests.get(f"{apiurl}", params=params)
    response=response.json()
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


def getinfo(colleges):
    '''
    Gets a list of 6 digit ope ids for colleges, returns list of json objects of college data
    using collegescorecard. 
    '''
    apiurl = "https://api.data.gov/ed/collegescorecard/v1/schools.json"
    params={}
    params["api_key"]=os.environ.get('api_key')
    collegeinfo=[]
    for college in colleges:
        params["ope6_id"]=college
        response = requests.get(f"{apiurl}", params=params)
        response=response.json()
        response=response["results"]
        response=response[0]
        collegeinfo.append(response)
    return collegeinfo


def getgraphdata(colleges,category,name):
    '''
    Gets graph x axis labels and height data from list of college 
    json objects and chosen category and attribute
    '''
    x=[]
    height=[]
    name=name.split(".")
    for college in colleges:
        college=college["latest"]
        try:
            collegename=college["school"]["name"]
            college=college[category]
            for part in name:
                college=college[part]
            x.append(collegename)
            if college!=None:
                height.append(college)
            else:
                height.append(0)
            '''
            try:
                ht=ht["average"]
                ht=ht["overall"]
            except:
                pass
            try:
                ht=ht["overall"]
            except:
                pass
            height.append(float(ht))
            x.append(college["school"]["name"])
            '''
        except:
            print("hell nah")
            pass

    return(x,height)

def getgraphcolors(colleges):
    colors=[]
    for college in colleges:
        college=college["latest"]
        try:
            imgurl=college["school"]["school_url"]
            if(imgurl[0:4]!="http"):
                imgurl="https://"+imgurl
            print(imgurl)
            color=getfaviconcolor(imgurl)
            if(color[0:3]!=[255,255,255]):
                color1=[]
                for x in range(len(color)):
                    color1.append(color[x]/255.0)
                colors.append(color1)
            else:
                colors.append([0.0, 0.0, 0.0])
        except:
            colors.append([0.0, 0.0, 0.0])
    print(colors)
    return colors


def savegraph(x, height,color):
    plt.bar(x=x,height=height,color=color)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("static/my_plot.png")
    plt.close()
    return 0


def bargraph(x,height):
    '''
    Turns x axis labels and height data into bar graph
    '''
    plt.bar(x=x,height=height)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()




def getfaviconcolor(url):
    icons = favicon.get(url)
    icon = icons[0]
    response = requests.get(icon.url, stream=True)
    #with open('tmp/favicon.{}'.format(icon.format), 'wb') as image:
    with open('tmp/favicon.png', 'wb') as image:
        for chunk in response.iter_content(1024):
            image.write(chunk)
    #with Image.open('tmp/favicon.{}'.format(icon.format)) as pil_img:
    with Image.open('tmp/favicon.png') as pil_img:
        img = pil_img.copy()
         # Reduce colors (uses k-means internally)
        paletted = img.convert('P', palette=Image.ADAPTIVE, colors=16)
        # Find the color that occurs most often
        palette = paletted.getpalette()
        color_counts = sorted(paletted.getcolors(), reverse=True)
        palette_index = color_counts[0][1]
        dominant_color = palette[palette_index*3:palette_index*3+3]
        print(dominant_color)
        return dominant_color


        '''
        img = pil_img.copy()



        img = img.convert("RGBA")
        img = img.resize((1, 1), resample=0)
        dominant_color = img.getpixel((0, 0))
        return dominant_color

    
    pil_img=Image.open(icon,mode='r',formats=None)
    img=pil_image.copy()
    img=img.convert("RGBA")
    img=img.resize((1,1),resample=0)
    dominant_color=img.getpixel((0,0))
    return dominant_color
    '''
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
    