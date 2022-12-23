from flask.blueprints import Blueprint
from requests import request
import os
import ipinfo
from flask import make_response,render_template,url_for
from datetime import datetime,timedelta
import requests as r
import json
import ipinfo
from flask import current_app,request
main = Blueprint('main',__name__)

def get_cookie():
    """
    1.Get user ip (if it's tested locally it reads it from config file).
    2.Read localisation information using API.
    3.Set cookie with duration 30 days.
    """
    ip_address =  request.environ['REMOTE_ADDR']
    print(ip_address)
    if ip_address == "127.0.0.1":
        print(os.environ.get('random_ip_address'))
        ip_address=os.environ.get('random_ip_address')
    #     print(ip_address)
    access_token = os.environ.get('ipinfo_key')
    handler = ipinfo.getHandler(access_token=access_token)
    details = handler.getDetails(ip_address=ip_address)
    resp = make_response(render_template('base.html'))

    resp.set_cookie('ip',ip_address,expires=datetime.now()+timedelta(days=30))
    current_app.logger.info("Creating cookies...")
    if ip_address != "127.0.0.1":
        resp.set_cookie('city',details.city,expires=datetime.now() + timedelta(days=30))
        resp.set_cookie('postal',details.postal,expires=datetime.now() + timedelta(days=30))
        resp.set_cookie('latitude',details.latitude,expires=datetime.now() + timedelta(days=30))
        resp.set_cookie('longitude',details.longitude,expires=datetime.now() + timedelta(days=30))
    current_app.logger.info("Cookies has been created.")
    return resp

def check_cookie():
        """
        Check's whether cookie exists and if it means that cookies are created on this browser.
        """
        print(request)
        current_app.logger.info("Checking cookies...")
        if 'city' in request.cookies:
            current_app.logger.info("Cookies already exists.")
        else:
            current_app.logger.info("No cookie found.Creating new ones...")
            return get_cookie()

def get_weather():
    """
    1.Get created cookies by get_cookie()
    2.Make call with generated api key
    3.Convert it to json
    4.Enumerate through it and catch wanted informations and push it to previous created dictionary
    """
    latitude = request.cookies.get('latitude')
    longitude = request.cookies.get('longitude')
    city = request.cookies.get('city')
    postal = request.cookies.get('postal')
    weather_key = os.environ.get('weatherapi')

    url="https://api.weatherapi.com/v1/forecast.json?key=%s&q=%s,%s&days=1&aqi=no&alerts=no"%(weather_key,latitude,longitude)
    response = r.get(url)
    weather = response.json()
    weather_dataset = {"timezone":"","now":{"last_updated":"","temp_c":"","condition_text":"","condition_icon":""},
    "days":[]}

    for count,day in enumerate(weather["forecast"]["forecastday"]):
        info = {"pressure":[],"wind_kph":[],"time":[],"temp_c":[],"feelslike_c":[],"condition":{"name":[],"icon":[]},"chance_of_rain":[],"chance_of_snow":[]}
        for x_hour in day['hour']:
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
    response = r.get(url)
    weather = response.json()
    weather_dataset["timezone"] = weather["location"]["tz_id"]
    weather_dataset["now"]["last_updated"] = weather["current"]["last_updated"]
    weather_dataset["now"]["last_updated"] = weather_dataset["now"]["last_updated"].split(' ')[1]
    weather_dataset["now"]["temp_c"] = round(weather["current"]["temp_c"])
    weather_dataset["now"]["condition_text"] = weather["current"]["condition"]["text"]
    weather_dataset["now"]["condition_icon"] = weather["current"]["condition"]["icon"]
    current_app.logger.info("Got weather data informations")
    print(weather_dataset['days'][0]['condition']['icon'][7])
    return weather_dataset





@main.route('/success')
def success():
    return render_template('error-success-pages/success.html')

@main.route('/')
def base():
    check_cookie()
    return render_template('base.html')
    

@main.route('/one')

def one():

    current_app.logger.info("Checking cookies...")
    if 'city' in request.cookies:
        current_app.logger.info("Cookies already exists.")
        one_day_dataset =get_weather()
        with open("app/static/one_day.json",'w',encoding='utf-8') as f:
            json.dump(one_day_dataset,f)

        google_key = os.environ.get('googleapi')
        return render_template('subpages/one_2ndapi.html',day = one_day_dataset, google_key=google_key)  # rendered html and function get_weather that returns json with all needed information 
    else:
        return get_cookie()