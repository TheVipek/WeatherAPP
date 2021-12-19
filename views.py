from typing import Type
from flask.helpers import url_for
from flask import flash
from werkzeug.utils import redirect
from werkzeug.wrappers import response
from wtforms.fields.simple import SubmitField
from app import app
from flask import  render_template,request,make_response,session
import requests ,ipinfo,os,math,json
from datetime import datetime, timedelta
from models import *
from wtforms import Form,BooleanField,StringField,PasswordField,EmailField,validators
from werkzeug.security import generate_password_hash,check_password_hash
from models import Accounts


class RegistrationForm(Form):
    username = StringField('Username',validators=[validators.length(min=8,max=24),validators.DataRequired()])
    password = PasswordField('Password',validators=[validators.length(min=8,max=32),
    validators.EqualTo('re_password','Make sure passwords are the same'),validators.DataRequired()])
    re_password = PasswordField('Repeat Password')
    email = EmailField('E-mail',validators=[validators.length(max=50),
    validators.EqualTo('re_email','Make sure e-mail is the same'),validators.DataRequired()])
    re_email =EmailField('Repeat E-mail')
    newsletter = BooleanField('Want join to newsletter? (Informations about updates in first place!)')
    submit = SubmitField('Register')

class LoginForm(Form):
    username =StringField('Username',validators=[validators.DataRequired()])
    password = PasswordField('Password',validators=[validators.DataRequired()])
    Remember_Me=BooleanField('Remember Me')
    submit = SubmitField('Sign In')

def get_cookie():
    # ip_address = request.environ['REMOTE_ADDR']
    ip_address = "185.12.21.170"
    access_token = os.environ.get('ipinfo_key')
    handler = ipinfo.getHandler(access_token=access_token)
    details = handler.getDetails(ip_address=ip_address)
    resp = make_response(render_template('base.html'))
    resp.set_cookie('ip',ip_address,expires=datetime.now()+timedelta(days=30))
    app.logger.info("Creating cookies...")

    if ip_address!='127.0.0.1':
        resp.set_cookie('city',details.all['city'],expires=datetime.now() + timedelta(days=30))
        resp.set_cookie('postal',details.all['postal'],expires=datetime.now() + timedelta(days=30))
        resp.set_cookie('latitude',details.all['latitude'],expires=datetime.now() + timedelta(days=30))
        resp.set_cookie('longitude',details.all['longitude'],expires=datetime.now() + timedelta(days=30))
        app.logger.info("Cookies has been created.")
    return resp

def check_cookie():
        app.logger.info("Checking cookies...")
        if 'city' in request.cookies:
            app.logger.info("Cookies already exists.")
        else:
            app.logger.info("No cookie found.Creating new ones...")
            return get_cookie()
    


def get_weather():
    

    # latitude = session['latitude']
    # longtitude = session['longtitude']
    # city = session['city']
    # postal = session['postal']

    latitude = request.cookies.get('latitude')
    longitude = request.cookies.get('longitude')
    city = request.cookies.get('city')
    postal = request.cookies.get('postal')
    weather_key = os.environ.get('weatherapi')

    url="https://api.weatherapi.com/v1/forecast.json?key=%s&q=%s,%s&days=1&aqi=no&alerts=no"%(weather_key,latitude,longitude)
    response = requests.get(url)
    weather = response.json()
    weather_dataset = {"timezone":"","now":{"last_updated":"","temp_c":"","condition_text":"","condition_icon":""},
    "days":[]}

    # weather_dataset["current"]["last_updated"] = weather["current"]["last_updated"].split(' ')[1]
    # weather_dataset["current"]["temp_c"] = round(weather["current"]["temp_c"])
    # weather_dataset["current"]["condition"]["name"] = weather["current"]["condition"]["text"]
    # weather_dataset["current"]["condition"]["icon"] = weather["current"]["condition"]["icon"]

    for count,day in enumerate(weather["forecast"]["forecastday"]):
        info = {"pressure":[],"wind_kph":[],"time":[],"temp_c":[],"feelslike_c":[],"condition":{"name":[],"icon":[]},"chance_of_rain":[],"chance_of_snow":[]}
        for x_hour in day['hour']:
            # print(math.ceil(x_hour['pressure_mb']))
            # print(math.ceil(x_hour['wind_kph']))
            # print(x_hour['time'].split(' ')[1])
            # print(math.ceil(x_hour['temp_c']))
            # rounded_temp = x_hour['temp_c']
            # {"pressure":[],"wind_kph":[],"time":[],"temp_c":[],"condition":{"name":[],"icon":[]}}
            info["pressure"].append(round(x_hour['pressure_mb']))
            info["wind_kph"].append(round(x_hour['wind_kph']))
            info["time"].append(x_hour['time'].split(' ')[1])
            info["temp_c"].append(round(x_hour['temp_c']))
            info["condition"]["name"].append(x_hour['condition']["text"])
            info["condition"]["icon"].append(x_hour['condition']["icon"])
            info["chance_of_rain"].append(x_hour["chance_of_rain"])
            info["chance_of_snow"].append(x_hour["chance_of_snow"])
            info["feelslike_c"].append(x_hour["feelslike_c"])
        weather_dataset["days"].append(info)
    
    url="https://api.weatherapi.com/v1/current.json?key=%s&q=%s,%s&aqi=no&alerts=no"%(weather_key,latitude,longitude)
    response = requests.get(url)
    weather = response.json()
    weather_dataset["timezone"] = weather["location"]["tz_id"]
    weather_dataset["now"]["last_updated"] = weather["current"]["last_updated"]
    weather_dataset["now"]["last_updated"] = weather_dataset["now"]["last_updated"].split(' ')[1]
    weather_dataset["now"]["temp_c"] = round(weather["current"]["temp_c"])
    weather_dataset["now"]["condition_text"] = weather["current"]["condition"]["text"]
    weather_dataset["now"]["condition_icon"] = weather["current"]["condition"]["icon"]

    # json_weather = json.dumps(weather_dataset)
    
    # with open ('static/weather_data.json','w') as to_save:
    #     json.dump(weather_dataset,to_save)
    app.logger.info("Got weather data informations")
    print(weather_dataset['days'][0]['condition']['icon'][7])
    return weather_dataset






# @app.route('/admin_panel')
# def admin():
#     cursor = 

@app.route('/login' ,methods=["GET","POST"])
def login():
    # users = Accounts.query.all()
    # for user in users:
    #     db.session.delete(user)
    #     db.session.commit()
    # for user in users:
    #     print("asd")
    #     print(user);
    # print("asd")
    form = LoginForm(request.form)

    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data
            users = Accounts.query.all()
            for user in users:
                if username == user.username:
                    fetch = Accounts.query.filter_by(username=username).first()
                    if check_password_hash(fetch.password,password):
                        flash('Sucessfully logged in!')
                        return redirect(url_for('base'))
            else:
                flash('Username or password is wrong.')
                return render_template('login.html',form=form)
                
                
    return render_template('login.html',form=form)

@app.route('/register',methods=['POST','GET'])
def register():
    registration = RegistrationForm(request.form)
    if request.method == "POST":
        if registration.validate():
            app.logger.info("Getting username...")
            username = registration.username.data
            app.logger.info("Getting email...")
            email = registration.email.data
            if username in Accounts.query.all():
                flash('Username is already used.','error')
                return render_template('register.html',form=registration)
            elif email in Accounts.query.all():
                flash('Email is already used.','error')
                return render_template('register.html',form=registration)
            else:
                app.logger.info("Getting password...")
                password_hash = generate_password_hash(registration.password.data)
                app.logger.info("Getting newsletter value...")
                newsletter = registration.newsletter.data
                user = Accounts(username=username,email=email,password=password_hash,newsletter=newsletter)
                db.session.add(user)
                db.session.commit()
                flash('Thanks for registering')
                return redirect(url_for('success'))
                
    return render_template('register.html',form = registration)

@app.route('/success')
def success():
    form = LoginForm()
    return render_template('success.html' ,form=form)


@app.route('/')
def base():
    app.logger.info("Checking cookies...")
    if 'city' in request.cookies:
        app.logger.info("Cookies already exists.")
        return render_template('base.html')
    else:
        return get_cookie()
    
        


@app.route('/one')
# def one():
#     w_data = get_weather()
#     print(w_data)
#     google_key = os.environ.get('googleapi')
#     return render_template('one.html',w_data = w_data["current"], google_key=google_key)  # rendered html and function get_weather that returns json with all needed information 
    #   now = get_openweather()[0]
    #   hourly = get_openweather()[1]
    # weather =get_weather()
    # print(weather);
    # google_key = os.environ.get('googleapi')
    #   return render_template('one.html',now = now ,hourly = hourly, google_key=google_key)  # rendered html and function get_weather that returns json with all needed information  
    #about weather




def one():
    # app.logger.info("Checking cookies...")
    # if 'city' in request.cookies:
    #     app.logger.info("Cookies already exists.")
    # else:
    #     app.logger.info("No cookie found.Creating new ones...")
    #     get_cookie()
    app.logger.info("Checking cookies...")
    if 'city' in request.cookies:
        app.logger.info("Cookies already exists.")
        one_day_dataset =get_weather()
        with open('static/one_day.json','w',encoding='utf-8') as f:
            json.dump(one_day_dataset,f)

        google_key = os.environ.get('googleapi')
        return render_template('one_2ndapi.html',day = one_day_dataset, google_key=google_key)  # rendered html and function get_weather that returns json with all needed information 
    else:
        return get_cookie()
    
 
