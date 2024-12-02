from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

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
    res_base=f"广州市{lives['city']}   当前天气：{lives['weather']}   温度：{lives['temperature']}   风向：{lives['winddirection']}   \
风力级别：{lives['windpower']}   空气湿度：{lives['humidity']}"
    
    res_forecasts=f"广州市{forecasts['city']}   明天白天天气：{forecasts['casts'][0]['dayweather']}   明天晚上天气：{forecasts['casts'][0]['nightweather']}   \
明天白天温度：{forecasts['casts'][0]['daytemp']}   明天晚上温度：{forecasts['casts'][0]['nighttemp']}"
    
    return tem_time,f'{res_base}\n{res_forecasts}'

def two_city_weather(code_city1,code_city2):
    tem_time1,res1= get_weather(code_city1)
    tem_time2,res2= get_weather(code_city2)
    return tem_time1+'\n'+res1+'\n\n'+res2


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
weather= two_city_weather(code_city1,code_city2)

love_days=love_count()
# print(love_days)

birthday_left=get_birthday()
# print(birthday_left)

words=get_words()
# print(words)

color=get_random_color()
# print(color)

data = {"weather":{"value":weather+'\n\n'},"love_days":{"value":love_days},"birthday_left":{"value":birthday_left},"words":{"value":words, "color":color}}
print(data)
res = wm.send_template(user_id, template_id, data)
print(res)
