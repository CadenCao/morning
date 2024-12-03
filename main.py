from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = '2024-09-22 19:00:00'
# start_date = os.environ['START_DATE']

city = os.environ['CITY']
print(city)
birthday = '03-12'
# birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
print(app_id)
app_id = 'wxfdda80846713c1ca'

app_secret = '1660ddba6b8258c445dc10bf44261cbd'
# app_secret = os.environ["APP_SECRET"]

user_id = 'oZBrP6Ebt1GcssGf2Yf_JiUFbXKg'
# user_id = os.environ["USER_ID"]
template_id1 = 'UyBorfAxWpQti74dhPbfUPFsdyiiojvFmI4GjRHvfXo'
template_id2 = 'oy7rtiU0U0vENmlmRUI1wUkG2RuSVmf_ILQdtK6BUdg'
# template_id = os.environ["TEMPLATE_ID"]

key='183ab5e8e01d6f3876be06ad207c7298'

def get_weather(code_city):
    code,city=code_city
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={key}&city={code}&extensions=base"
    res_get_base = requests.get(url).json()
    lives=res_get_base['lives'][0]


    url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={key}&city={code}&extensions=all"
    res_get_forecast = requests.get(url).json()
    forecasts=res_get_forecast['forecasts'][0]
    
    tem_time=f"时间：{lives['reporttime']}"
    

#     res_base=f"广州市{lives['city']}   当前天气：{lives['weather']}   温度：{lives['temperature']}   风向：{lives['winddirection']}   \
# 风力级别：{lives['windpower']}   空气湿度：{lives['humidity']}"
    city,weather,temperature=f'广州市{lives['city']}',lives['weather'],lives['temperature']
    winddirection,windpower,humidity=lives['winddirection'],lives['windpower'],lives['humidity']

#         res_forecasts=f"广州市{forecasts['city']}   明天白天天气：{forecasts['casts'][0]['dayweather']}   明天晚上天气：{forecasts['casts'][0]['nightweather']}   \
# 明天白天温度：{forecasts['casts'][0]['daytemp']}   明天晚上温度：{forecasts['casts'][0]['nighttemp']}"
    city_forecasts,dayweather_forecasts,nightweather_forecasts=f"广州市{forecasts['city']}",forecasts['casts'][0]['dayweather'],forecasts['casts'][0]['nightweather']
    daytemp_forecasts,nighttemp_forecasts=forecasts['casts'][0]['daytemp'],forecasts['casts'][0]['nighttemp']

    # return tem_time,f'{res_base}\n{res_forecasts}'
    return [city,weather,temperature,winddirection,windpower,humidity,  \
city_forecasts,dayweather_forecasts,nightweather_forecasts,daytemp_forecasts,nighttemp_forecasts]

def two_city_weather(code_city1,code_city2):
    res1= get_weather(code_city1)
    res2= get_weather(code_city2)
    return res1+res2
    # return tem_time1+'\n'+res1+'\n\n'+res2


def love_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)
    
client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)

def send_measage(user_id,template_id,data):
    res = wm.send_template(user_id, template_id, data)
    print(data)

love_days=love_count()

birthday_left=get_birthday()

words=get_words()

color=get_random_color()
print(love_days,birthday_left,words)

code_city1 = ('440112','黄浦区')
code_city2 = ('440106','天河区')
city1,weather1,temperature1,winddirection1,windpower1,humidity1,city_forecasts1,dayweather_forecasts1,nightweather_forecasts1,daytemp_forecasts1,nighttemp_forecasts1, \
city2,weather2,temperature2,winddirection2,windpower2,humidity2,ity_forecasts2,dayweather_forecasts2,nightweather_forecasts2,daytemp_forecasts2,nighttemp_forecasts2= two_city_weather(code_city1,code_city2)


data = {"love_days":{"value":love_days},"birthday_left":{"value":birthday_left},"words":{"value":words},
        'weather_city1':{"value":city1},'weather_weather1':{"value":weather1},'weather_temperature1':{"value":temperature1},
        'weather_winddirection1':{"value":winddirection1},'weather_windpower1':{"value":windpower1},'weather_humidity1':{"value":humidity1},
        'weather_city_forecasts1':{"value":city_forecasts1},'weather_dayweather_forecasts1':{"value":dayweather_forecasts1},
       'weather_nightweather_forecasts1':{"value":nightweather_forecasts1},'weather_daytemp_forecasts1':{"value":daytemp_forecasts1},'weather_nighttemp_forecasts1':{"value":nighttemp_forecasts1},
       'weather_city2':{"value":city2},'weather_weather2':{"value":weather2},'weather_temperature2':{"value":temperature2},
        'weather_winddirection2':{"value":winddirection2},'weather_windpower2':{"value":windpower2},'weather_humidity2':{"value":humidity2},
        'weather_city_forecasts2':{"value":city_forecasts2},'weather_dayweather_forecasts2':{"value":dayweather_forecasts2},
       'weather_nightweather_forecasts2':{"value":nightweather_forecasts2},'weather_daytemp_forecasts2':{"value":daytemp_forecasts2},'weather_nighttemp_forecasts2':{"value":nighttemp_forecasts2}}



send_measage(user_id,template_id1,data)
send_measage(user_id,template_id2,data)

