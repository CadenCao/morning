from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = '2024-09-21 00:00:01'
meet_data='2024-08-31 00:00:01'
birthday = '03-12'

app_id = 'wxfdda80846713c1ca'
app_secret = '1660ddba6b8258c445dc10bf44261cbd'

user_id1 = 'oZBrP6Ebt1GcssGf2Yf_JiUFbXKg'
user_id2 = 'oZBrP6NmYGuREGxGPOykkETbmrbU'

template_id1 = 'ca1nmLCYiuGYjSuekXITbuImaRT65WhNRO1GL9CC6ho'
template_id2 = '7wiwcBbLwAVSGJ8GftX5FFTt0mk4ufsqY0Sl-3vjBcs'


key='183ab5e8e01d6f3876be06ad207c7298'

# def get_weather(code_city):
#     code,city=code_city
#     url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={key}&city={city}&extensions=base"
#     res_get_base = requests.get(url).json()
#     lives=res_get_base['lives'][0]


#     url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={key}&city={city}&extensions=all"
#     res_get_forecast = requests.get(url).json()
#     forecasts=res_get_forecast['forecasts'][0]
    
#     tem_time=f"时间：{lives['reporttime']}"

#     city,weather,temperature=f'{lives['city']}',lives['weather'],lives['temperature']
#     winddirection,windpower,humidity=lives['winddirection'],lives['windpower'],lives['humidity']

#     city_forecasts,dayweather_forecasts,nightweather_forecasts=f"{forecasts['city']}",forecasts['casts'][0]['dayweather'],forecasts['casts'][0]['nightweather']
#     daytemp_forecasts,nighttemp_forecasts=forecasts['casts'][0]['daytemp'],forecasts['casts'][0]['nighttemp']

#     return [city,weather,temperature,winddirection,windpower,humidity,  \
# city_forecasts,dayweather_forecasts,nightweather_forecasts,daytemp_forecasts,nighttemp_forecasts]

def get_weather(code_city):
    code,city=code_city
    url = f'https://devapi.qweather.com/v7/weather/3d?location={code}&key=249dd226faf44d4d93132cffd8744689'
    res_get_base = requests.get(url).json()
    lives=res_get_base['daily'][1]
    fxDate,moonPhase,tempMax,tempMin,textDay,textNight,windScaleDay,uvIndex,humidity= \
lives['fxDate'],lives['moonPhase'],lives['tempMax'],lives['tempMin'],lives['textDay'], \
lives['textNight'],lives['windScaleDay'],lives['uvIndex'],lives['humidity'],
    
    return [city,fxDate,moonPhase,tempMax,tempMin,textDay,textNight,windScaleDay,uvIndex,humidity]

def love_count():
  delta1 = today - datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
  days,hours,minutes =delta1.days,delta1.seconds // 3600,delta1.seconds % 3600 // 60
  res1=f'{days+1}天'
  delta2 = today - datetime.strptime(meet_data, "%Y-%m-%d %H:%M:%S")
  days,hours,minutes =delta2.days,delta2.seconds // 3600,delta2.seconds % 3600 // 60
  res2=f'{days+1}'
  return res1,res2

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

def get_tips(textDay,textNight,temperature,humidity,uvIndex):
    res=[]
    if '雨' in textDay or '雨' in textNight:
        res.append('宝宝，明天有雨哦，记得带伞，小心着凉')
    else:
        if int(temperature)>24:
            res.append('宝宝，明天很暖和哦')
        elif 15<=int(temperature)<=24:
            res.append('宝宝，明天很舒适哦')
        elif 10<=int(temperature)<15:
            res.append('宝宝，明天可能有点冷，多穿点衣服')
        else:
            res.append('宝宝，明天很冷，直接上羽绒服')
    if int(humidity)<=40:
        res.append(f'宝宝，明天空气很干，记得随身携带保湿产品')
    elif 50>=int(humidity)>40:
        res.append(f'宝宝，明天空气偏干，记得涂点保湿的再出门')
    elif 70>=int(humidity)>50:
        res.append(f'宝宝，明天空气适中，可以根据个人情况保湿')
    else:
        res.append(f'宝宝，明天空气很润，保湿可以随意')
    if int(uvIndex)<=2:
        res.append(f'宝宝，明天紫外线很弱，大胆出门')
    elif 4>=int(uvIndex)>=3:
        res.append(f'宝宝，明天紫外线偏弱，不用担心')
    elif 6>=int(uvIndex)>=5:
        res.append(f'宝宝，明天紫外线较强，注意防晒')
    elif 9>=int(uvIndex)>=7:
        res.append(f'宝宝，明天紫外线很强，可以防晒霜+伞走起')
    else:
        res.append(f'宝宝，明天紫外线超强，需要防晒武装到牙齿了')
    return res
    
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)
    
client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)

def send_measage(user_id,template_id,data):
    res = wm.send_template(user_id, template_id, data)
    print(data)

love_days,meet_days=love_count()

birthday_left=get_birthday()

# code_city1 = ('440112','黄埔区')
# code_city2 = ('440106','天河区')


'''
黄埔：101280111
天河：101280109
'''
code_city=('101280111','广州市黄埔区')

city,fxDate,moonPhase,tempMax,tempMin,textDay,textNight,windScaleDay,uvIndex,humidity=get_weather(code_city)

tips=get_tips(textDay,textNight,tempMax,humidity,uvIndex)


data = {"love_days":{"value":love_days},"birthday_left":{"value":birthday_left},"meet_days":{"value":meet_days},
        "city":{"value":city},"fxDate":{"value":fxDate},"moonPhase":{"value":moonPhase},
        "tempMax":{"value":tempMax},"tempMin":{"value":tempMin},"textDay":{"value":textDay},
        "textNight":{"value":textNight},"windScaleDay":{"value":windScaleDay},
        "uvIndex":{"value":uvIndex},"humidity":{"value":humidity},
        "tips0":{"value":tips[0]},"tips1":{"value":tips[1]},"tips2":{"value":tips[2]}
       }



send_measage(user_id1,template_id1,data)
send_measage(user_id2,template_id1,data)

