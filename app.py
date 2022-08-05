from flask import Flask, render_template, request,g,url_for,flash,redirect,session,make_response
import re
import requests 
import forms
import helper
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
from choices import getData
import favicon
import json

colleges = requests.get("http://universities.hipolabs.com/search?country=United+States").json()
collegelist = []
for i in colleges:
    collegelist.append(i['name'].split(',')[0])

info_ids_available = "acceptance_rate,act_cumulative_midpoint,act_cumulative_percentile25,act_cumulative_percentile75,admissions_website,aliases,application_website,average_aid_awarded_high_income,average_aid_awarded_lower_middle_income,average_aid_awarded_low_income,average_aid_awarded_middle_income,average_aid_awarded_upper_middle_income,average_financial_aid,avg_cost_of_attendance,avg_net_price,calendar_system,campus_image,city,class_size_range10_to19,class_size_range20_to29,class_size_range2_to9,class_size_range30_to39,class_size_range40_to49,class_size_range50_to99,class_size_range_over100,demographics_men,demographics_women,financial_aid_website,four_year_graduation_rate,fraternities_percent_participation,freshmen_live_on_campus,in_state_tuition,is_private,meal_plan_available,median_earnings_six_yrs_after_entry,median_earnings_ten_yrs_after_entry,men_varsity_sports,net_price_by_income_level0_to3000,net_price_by_income_level110001_plus,net_price_by_income_level30001_to48000,net_price_by_income_level48001_to75000,net_price_by_income_level75001_to110000,offers_study_abroad,on_campus_housing_available,out_of_state_tuition,percent_of_students_who_receive_financial_aid,percent_students_receiving_federal_grant_aid,percent_undergrads_awarded_aid,rankings_best_college_academics,rankings_best_college_athletics,rankings_best_college_campuses,rankings_best_college_food,rankings_best_college_locations,rankings_best_college_professors,rankings_best_colleges,rankings_best_colleges_for_art,rankings_best_colleges_for_biology,rankings_best_colleges_for_business,rankings_best_colleges_for_chemistry,rankings_best_colleges_for_communications,rankings_best_colleges_for_computer_science,rankings_best_colleges_for_design,rankings_best_colleges_for_economics,rankings_best_colleges_for_engineering,rankings_best_colleges_for_history,rankings_best_colleges_for_nursing,rankings_best_colleges_for_physics,rankings_best_greek_life_colleges,rankings_best_student_athletes,rankings_best_student_life,rankings_best_test_optional_colleges,rankings_best_value_colleges,rankings_colleges_that_accept_the_common_app,rankings_colleges_with_no_application_fee,rankings_hardest_to_get_in,rankings_hottest_guys,rankings_most_conservative_colleges,rankings_most_liberal_colleges,rankings_most_diverse_colleges,rankings_top_party_schools,region,sat_average,sat_composite_midpoint,sat_composite_percentile25,sat_composite_percentile75,sat_math_midpoint,sat_math_percentile25,sat_math_percentile75,sat_reading_midpoint,sat_reading_percentile25,sat_reading_percentile75,student_faculty_ratio,students_submitting_a_c_t,students_submitting_s_a_t,type_year,typical10_year_earnings,typical6_year_earnings,typical_books_and_supplies,typical_financial_aid,typical_misc_expenses,typical_room_and_board,undergrad_application_fee,undergraduate_size,women_only,women_varsity_sports".replace(',', '%2C')
basic_ids_available = "campus_image,website,long_description,aliases,city,stateAbbr,region".replace(',', '%2C')
admission_ids_available =  "acceptance_rate,gpa_requirement,type_year,type_category,men_only,religious_affiliation,sat_average,students_submitting_a_c_t,students_submitting_s_a_t,sat_math_midpoint,sat_reading_midpoint,act_cumulative_midpoint,act_cumulative_percentile25,act_cumulative_percentile75,undergrad_application_fee,application_website".replace(',', '%2C')
pricing_ids_available = "in_state_tuition,out_of_state_tuition,avg_cost_of_attendance,avg_net_price,percent_undergrads_awarded_aid,average_aid_awarded_high_income,average_aid_awarded_lower_middle_income,average_aid_awarded_low_income,average_aid_awarded_middle_income,average_aid_awarded_upper_middle_income,net_price_by_income_level0_to3000,net_price_by_income_level110001_plus,net_price_by_income_level30001_to48000,net_price_by_income_level48001_to75000,net_price_by_income_level75001_to110000,typical_misc_expenses,typical_books_and_supplies,financial_aid_website".replace(',', '%2C')
campus_ids_available = "on_campus_housing_available,typical_room_and_board,freshmen_required_to_live_on_campus,undergraduate_size,freshmen_live_on_campus,meal_plan_available,student_faculty_ratio".replace(',', '%2C')
outcomes_ids_available = "four_year_graduation_rate,typical6_year_earnings,typical10_year_earnings".replace(',', '%2C')
sports_ids_available = "men_varsity_sports,women_varsity_sports,athletic_conference,fraternities_percent_participation".replace(',', '%2C')
rankings_ids_available ="rankings_best_college_academics,rankings_best_college_athletics,rankings_best_college_campuses,rankings_best_college_food,rankings_best_college_locations,rankings_best_college_professors,rankings_best_colleges,rankings_best_colleges_for_art,rankings_best_colleges_for_biology,rankings_best_colleges_for_business,rankings_best_colleges_for_chemistry,rankings_best_colleges_for_communications,rankings_best_colleges_for_computer_science,rankings_best_colleges_for_design,rankings_best_colleges_for_economics,rankings_best_colleges_for_engineering,rankings_best_colleges_for_history,rankings_best_colleges_for_nursing,rankings_best_colleges_for_physics,rankings_best_greek_life_colleges,rankings_best_student_athletes,rankings_best_student_life,rankings_best_test_optional_colleges,rankings_best_value_colleges,rankings_colleges_that_accept_the_common_app,rankings_colleges_with_no_application_fee,rankings_hardest_to_get_in,rankings_hottest_guys,rankings_most_conservative_colleges,rankings_most_liberal_colleges,rankings_most_diverse_colleges,rankings_top_party_schools".replace(',', '%2C')
similar_ids_available = "similar_colleges".replace(',', '%2C')

college_api_key = 'CeaWjQovErNUFi49b28QnYGk'

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

@app.route("/home",methods=("GET", "POST"))
@login_required
def home():

    #First card(close school that fit all the requirements)
    user_zipcode = current_user.address
    user_gpa = current_user.gpa
    sat_score = str(int(current_user.sat_math)+int(current_user.sat_reading_writing))
    distance = '60'
    degree_type = '4year'
    params = '{"satOverall":'+ sat_score +',"closeToMyScores":true,"distanceFromHomeMiles":[0,'+distance+'],"zipCode":'+user_zipcode+',"gpa-minimum-ten-percent":"'+user_gpa+'","degree-length":["'+ degree_type +'"]}'
    info_ids_params = "website,shortDescription,campusImage,city,stateAbbr,aliases,acceptance_rate,enrolled_students,avg_cost_of_attendance,average_financial_aid,logo_image"
    results = requests.get('https://api.collegeai.com/v1/api/college-list?api_key='+college_api_key + '&filters=' + requests.utils.quote(params)+'&info_ids='+info_ids_params)
    data = results.json()
    data = helper.filterCollegeData(data)
    
    #Search function and cookies
    form = forms.SearchForm()
    if form.validate_on_submit():
        search_query = form.search_query.data
        session["results"] = search_query
        try:
            return redirect(url_for("search_results"))
        except:
            print("Something went wrong") 

    return render_template("home.html",form = form,data = data)

@app.route("/search_results")
@login_required
def search_results():
    search_query = session['results']
    basic_query = get_college_info(search_query,basic_ids_available)
    admission_query = get_college_info(search_query,admission_ids_available)
    pricing_query = get_college_info(search_query,pricing_ids_available)
    campus_query = get_college_info(search_query,campus_ids_available )
    outcomes_query = get_college_info(search_query,outcomes_ids_available)
    sports_query = get_college_info(search_query,sports_ids_available )
    rankings_query = get_college_info(search_query,rankings_ids_available)
    similar_query = get_college_info(search_query,similar_ids_available)

    return render_template("search_results.html",basic_query=basic_query,admission_query=admission_query,pricing_query=pricing_query,campus_query=campus_query,outcomes_query=outcomes_query,sports_query=sports_query,rankings_query =rankings_query ,similar_query=similar_query)

@app.route("/registration",methods=("GET", "POST"))
def registration():
    form = forms.RegisterForm()
    if form.validate_on_submit():

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


@app.route("/advanced_search",methods=["GET","POST"])
@login_required
def advanced_search():
    form = forms.AdvancedSearchForm()
    if form.validate_on_submit():
        state = form.state.data
        school_type =form.school_type.data
        highest_degree =form.highest_degree.data
        #affiliated_religion =form.affiliated_religion.data
        campus_size = form.campus_size.data
        #diversity = form.diversity.data 
        acceptance_rate = form.acceptance_rate.data
        #annual_cost = form.annual_cost.data
        close_to_score = form.close_to_score.data
        #distance_from_home = form.distance_from_home.data

        types = f'"{school_type}"'
        size = f'"{campus_size}"'
        if close_to_score == True:
            score = 'true'
        else:
            score = 'false'
        zipcode = str(current_user.address)
        sat_score = str(int(current_user.sat_math)+int(current_user.sat_reading_writing))
        acceptance_type= f'"{acceptance_rate}"' 
        degree_type = f'"{highest_degree}"'


        info_ids_params = "website,shortDescription,campusImage,city,stateAbbr,aliases,acceptance_rate,enrolled_students,avg_cost_of_attendance,average_financial_aid,logo_image"
        params = '{"funding-type":[' + types + '],"schoolSize":['+ size +'],"satOverall":'+ sat_score +',"closeToMyScores":'+score+',"selectivity":['+ acceptance_type +'],"in-state":"'+state+'","degree-length":['+ degree_type +']}'
        results = requests.get('https://api.collegeai.com/v1/api/college-list?api_key='+college_api_key + '&filters=' + requests.utils.quote(params)+'&info_ids='+info_ids_params)
        session['results'] = json.dumps(results.json())
        return redirect(url_for("advanced_search_results"))

    
    return render_template("advanced_search.html", form=form)
    
@app.route("/advanced_search_results")
@login_required
def advanced_search_results():
    retrieve = session['results']
    data = json.loads(retrieve)
    data = helper.filterCollegeData(data)

    return render_template("advanced_search_results.html", data=data)


def get_college_info(college_name,ids):
    url = f'https://api.collegeai.com/v1/api/autocomplete/colleges?api_key={college_api_key}'
    json_data = requests.get(url + '&query='+college_name).json()
    info_ids_selector = ids
    #info_ids_selector1 covers admissions data
    invalid = {}
    
    try:
        college_id = json_data['collegeList'][0]['unitId']
    except:
        return invalid
    url = f'https://api.collegeai.com/v1/api/college/info?api_key={college_api_key}&college_unit_ids='+str(college_id)+'&info_ids='+info_ids_selector
    try:
        json_data = requests.get(url).json()['colleges'][0]
    except:
        return invalid

    return json_data

def putSpace(input):
    words = re.findall('[A-Z][a-z]*', input)
    # Change first letter of each word into lower
    # case
    for i in range(0,len(words)):
      words[i]=words[i][0].lower()+words[i][1:]
    return(' '.join(words))


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