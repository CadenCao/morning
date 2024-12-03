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

user_id1 = 'oZBrP6Ebt1GcssGf2Yf_JiUFbXKg'
user_id2 = 'oZBrP6NmYGuREGxGPOykkETbmrbU'
# user_id = os.environ["USER_ID"]
template_id1 = 'UfwyhrzREyfk9FObWtfmGB0K_lJcJJ5E7xWb0FO32KM'
template_id2 = '7wiwcBbLwAVSGJ8GftX5FFTt0mk4ufsqY0Sl-3vjBcs'
# template_id = os.environ["TEMPLATE_ID"]

key='183ab5e8e01d6f3876be06ad207c7298'

def get_weather(code_city):
    code,city=code_city
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={key}&city={city}&extensions=base"
    res_get_base = requests.get(url).json()
    lives=res_get_base['lives'][0]


    url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={key}&city={city}&extensions=all"
    res_get_forecast = requests.get(url).json()
    forecasts=res_get_forecast['forecasts'][0]
    
    tem_time=f"时间：{lives['reporttime']}"
    

#     res_base=f"广州市{lives['city']}   当前天气：{lives['weather']}   温度：{lives['temperature']}   风向：{lives['winddirection']}   \
# 风力级别：{lives['windpower']}   空气湿度：{lives['humidity']}"
    city,weather,temperature=f'{lives['city']}',lives['weather'],lives['temperature']
    winddirection,windpower,humidity=lives['winddirection'],lives['windpower'],lives['humidity']

#         res_forecasts=f"广州市{forecasts['city']}   明天白天天气：{forecasts['casts'][0]['dayweather']}   明天晚上天气：{forecasts['casts'][0]['nightweather']}   \
# 明天白天温度：{forecasts['casts'][0]['daytemp']}   明天晚上温度：{forecasts['casts'][0]['nighttemp']}"
    city_forecasts,dayweather_forecasts,nightweather_forecasts=f"{forecasts['city']}",forecasts['casts'][0]['dayweather'],forecasts['casts'][0]['nightweather']
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

def get_tips(weather1,temperature1,humidity1):
    res=[]
    if '雨'in weather1:
        res.append('宝宝，今天有雨哦，记得带伞，小心着凉。')
    else:
        if int(temperature1)>24:
            res.append('宝宝，今天很暖和哦！')
        elif 19<=int(temperature1)<=24:
            res.append('宝宝，今天很舒适哦！')
        elif 15<int(temperature1)<19:
            res.append('宝宝，今天可能有点冷，多穿点衣服！')
        else:
            res.append('宝宝，今天很冷，直接上羽绒服！')
    if int(humidity1)<=40:
        res.append(f'今天湿度{humidity1},很干，记得随身携带保湿产品！')
    elif 50>=int(humidity1)>40:
        res.append(f'今天湿度{humidity1},偏干，记得涂点保湿的再出门！')
    elif 60>=int(humidity1)>50:
        res.append(f'今天湿度{humidity1},适中，可以根据个人情况保湿。')
    else:
        res.append(f'今天湿度{humidity1},很润，保湿可以随意。')
    return res
    
        

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
# city1,weather1,temperature1,winddirection1,windpower1,humidity1,city_forecasts1,dayweather_forecasts1,nightweather_forecasts1,daytemp_forecasts1,nighttemp_forecasts1, \
# city2,weather2,temperature2,winddirection2,windpower2,humidity2,city_forecasts2,dayweather_forecasts2,nightweather_forecasts2,daytemp_forecasts2,nighttemp_forecasts2= two_city_weather(code_city1,code_city2)


city1,weather1,temperature1,winddirection1,windpower1,humidity1,city_forecasts1,dayweather_forecasts1,nightweather_forecasts1,daytemp_forecasts1,nighttemp_forecasts1=get_weather(code_city1)
tips=get_tips(weather1,temperature1,humidity1)


# data = {"love_days":{"value":love_days},"birthday_left":{"value":birthday_left},"words":{"value":words},
#         'city1':{"value":city1},'weather1':{"value":weather1},'temperature1':{"value":temperature1},
#         'winddirection1':{"value":winddirection1},'windpower1':{"value":windpower1},'humidity1':{"value":humidity1},
#         'city1':{"value":city_forecasts1},'dayweather1':{"value":dayweather_forecasts1},
#        'nightweather1':{"value":nightweather_forecasts1},'daytemp1':{"value":daytemp_forecasts1},'nighttemp1':{"value":nighttemp_forecasts1},
#        'city2':{"value":city2},'weather2':{"value":weather2},'temperature2':{"value":temperature2},
#         'winddirection2':{"value":winddirection2},'windpower2':{"value":windpower2},'humidity2':{"value":humidity2},
#         'city2':{"value":city_forecasts2},'dayweather2':{"value":dayweather_forecasts2},
#        'nightweather2':{"value":nightweather_forecasts2},'daytemp2':{"value":daytemp_forecasts2},'nighttemp2':{"value":nighttemp_forecasts2},
#         'tips':{"value":tips}
#        }

data = {"love_days":{"value":love_days},"birthday_left":{"value":birthday_left},"words":{"value":words},
        'city1':{"value":city1},'weather1':{"value":weather1},'temperature1':{"value":temperature1},
        'winddirection1':{"value":winddirection1},'windpower1':{"value":windpower1},'humidity1':{"value":humidity1},
        'city1':{"value":city_forecasts1},'dayweather1':{"value":dayweather_forecasts1},
       'nightweather1':{"value":nightweather_forecasts1},'daytemp1':{"value":daytemp_forecasts1},'nighttemp1':{"value":nighttemp_forecasts1},
        'tips':{"value":tips}
       }



send_measage(user_id1,template_id1,data)
send_measage(user_id2,template_id1,data)

