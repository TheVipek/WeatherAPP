from werkzeug.wrappers import response
from app import app
from flask import  render_template,request,make_response
import requests
import ipinfo
import os
import math
import json
from datetime import datetime


# def get_cookies():
#     ip_address = request.environ['REMOTE_ADDR']

# def get_openweather():
    # latitude = request.cookies.get('latitude')
    # longitude = request.cookies.get('longitude')
    # city = request.cookies.get('city')
    # postal = request.cookies.get('postal')
    # openweather_key = os.environ.get('openweather_key')
    # url = 'https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&units=metric&appid=%s'%(latitude,longitude,openweather_key)
    # response = requests.get(url)
    # weather = response.json()
    # print(weather)
    # now_dataset = {'name':"","current":{'temp':"",'pressure':"",'humidity':"",'wind':"",'description':"",'icon':""}}
    # now_dataset["name"] = weather["timezone"]
    # now_dataset["current"]["temp"] = math.floor(weather["current"]["temp"])
    # now_dataset["current"]["pressure"] = weather["current"]["pressure"]
    # now_dataset["current"]["humidity"] = weather["current"]["humidity"]
    # now_dataset["current"]["wind"] = math.floor(weather["current"]["wind_speed"])
    # now_dataset["current"]["description"] = weather["current"]["weather"][0]["description"]
    # now_dataset["current"]["icon"] = "http://openweathermap.org/img/wn/%s@4x.png"%(weather["current"]["weather"][0]["icon"])

    # hourly_days = []

    # daily_days = []

    # for hour in weather['hourly']:
    #     one_hour = {'temp':"","time":""}
    #     h = hour["dt"]
    #     h = datetime.fromtimestamp(h).strftime("%H:%M")
    #     temp = math.floor(hour["temp"])
    #     one_hour["temp"] = temp
    #     one_hour["time"] = h
    #     hourly_days.append(one_hour)
    
    # for day in weather["daily"]:
    #     one_day = {"time":"","temp":{"day":"","night":""},"pressure":"","humidity":"","wind_speed":"","pop":""}

    #     d = day["dt"]
    #     d = datetime.fromtimestamp(d).strftime("%d/%m")
    #     in_day = day["temp"]["day"]
    #     in_night = day["temp"]["night"]
    #     pressure = day["pressure"]
    #     humidity = day["humidity"]
    #     wind = day["wind_speed"]
    #     probability = day["pop"]

    #     one_day["time"] = d
    #     one_day["temp"]["day"] = in_day
    #     one_day["temp"]["night"] = in_night
    #     one_day["pressure"] = pressure
    #     one_day["humidity"] = humidity
    #     one_day["wind_speed"] = wind
    #     one_day["pop"] = probability
        
    #     daily_days.append(one_day)

    # return now_dataset,hourly_days,daily_days



def get_weather():
    latitude = request.cookies.get('latitude')
    longitude = request.cookies.get('longitude')
    city = request.cookies.get('city')
    postal = request.cookies.get('postal')
    weather_key = os.environ.get('weatherapi')

    url="https://api.weatherapi.com/v1/forecast.json?key=%s&q=%s,%s&days=%s&aqi=no&alerts=no"%(weather_key,latitude,longitude,1)
    response = requests.get(url)
    weather = response.json()

    weather_dataset = {"timezone":"","now":{"last_updated":"","temp_c":"","condition_text":"","condition_icon":""},"current":{'last_updated':"","temp_c":"","condition":{"name":"","icon":""}},
    "days":[]}

    weather_dataset["current"]["last_updated"] = weather["current"]["last_updated"].split(' ')[1]
    weather_dataset["current"]["temp_c"] = weather["current"]["temp_c"]
    weather_dataset["current"]["condition"]["name"] = weather["current"]["condition"]["text"]
    weather_dataset["current"]["condition"]["icon"] = weather["current"]["condition"]["icon"]

    for count,day in enumerate(weather["forecast"]["forecastday"]):
        info = {"pressure":[],"wind_kph":[],"time":[],"temp_c":[],"condition":{"name":[],"icon":[]}}
        for x_hour in day['hour']:
            # print(math.ceil(x_hour['pressure_mb']))
            # print(math.ceil(x_hour['wind_kph']))
            # print(x_hour['time'].split(' ')[1])
            # print(math.ceil(x_hour['temp_c']))
            # rounded_temp = x_hour['temp_c']
            # {"pressure":[],"wind_kph":[],"time":[],"temp_c":[],"condition":{"name":[],"icon":[]}}
            info["pressure"].append(math.ceil(x_hour['pressure_mb']))
            info["wind_kph"].append(math.ceil(x_hour['wind_kph']))
            info["time"].append(x_hour['time'].split(' ')[1])
            info["temp_c"].append(math.ceil(x_hour['temp_c']))
            info["condition"]["name"].append(x_hour['condition']["text"])
            info["condition"]["icon"].append(x_hour['condition']["icon"])
        weather_dataset["days"].append(info)
    
    url="https://api.weatherapi.com/v1/current.json?key=%s&q=%s,%s&aqi=no&alerts=no"%(weather_key,latitude,longitude)
    response = requests.get(url)
    weather = response.json()
    weather_dataset["timezone"] = weather["location"]["tz_id"]
    weather_dataset["now"]["last_updated"] = weather["current"]["last_updated"]
    weather_dataset["now"]["last_updated"] = weather_dataset["now"]["last_updated"].split(' ')[1]
    print(weather_dataset["now"]["last_updated"])
    weather_dataset["now"]["temp_c"] = weather["current"]["temp_c"]
    weather_dataset["now"]["condition_text"] = weather["current"]["condition"]["text"]
    weather_dataset["now"]["condition_icon"] = weather["current"]["condition"]["icon"]

    # json_weather = json.dumps(weather_dataset)
    
    # with open ('static/weather_data.json','w') as to_save:
    #     json.dump(weather_dataset,to_save)
    return weather_dataset




def get_cookie():
    ip_address = request.environ['REMOTE_ADDR']
    access_token = os.environ.get('ipinfo_key')
    handler = ipinfo.getHandler(access_token=access_token)
    details = handler.getDetails(ip_address=ip_address)
    resp = make_response(render_template('base.html'))
    resp.set_cookie('ip',ip_address)
    if ip_address!='127.0.0.1':
        resp.set_cookie('city',details.all['city'])
        resp.set_cookie('postal',details.all['postal'])
        resp.set_cookie('latitude',details.all['latitude'])
        resp.set_cookie('longitude',details.all['longitude'])
    return resp

def check_cookie():
    if 'city' in request.cookies:
        print('cookie found')
    else:
        return get_cookie()


@app.route('/')
def base():
    check_cookie()
    return render_template('base.html')


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
    check_cookie()
    one_day_dataset =get_weather()
    with open('static/one_day.json','w',encoding='utf-8') as f:
        json.dump(one_day_dataset,f)

    google_key = os.environ.get('googleapi')
    return render_template('one_2ndapi.html',day = one_day_dataset, google_key=google_key)  # rendered html and function get_weather that returns json with all needed information 
 
