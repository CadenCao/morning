import os
import random
import time
from datetime import datetime, timedelta, timezone
import requests
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage

# ==================== 环境变量读取 ====================
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
TEMPLATE_ID = os.getenv("TEMPLATE_ID")
USER_ID1 = os.getenv("USER_ID1")
USER_ID2 = os.getenv("USER_ID2")
WEATHER_KEY = os.getenv("WEATHER_KEY")          # 和风天气 key
START_DATE = os.getenv("START_DATE")            # 恋爱开始日期
MEET_DATE = os.getenv("MEET_DATE")              # 相遇日期
BIRTHDAY = os.getenv("BIRTHDAY")                # 生日，如 03-12
CITY_CODE = os.getenv("CITY_CODE", "101280111") # 城市代码

# ==================== 北京时间工具 ====================
BEIJING_TZ = timezone(timedelta(hours=8))

def get_beijing_now():
    return datetime.now(BEIJING_TZ)

# ==================== 天气获取 ====================
def get_weather(city_code):
    """获取明天天气"""
    url = f"https://devapi.qweather.com/v7/weather/3d?location={city_code}&key={WEATHER_KEY}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    
    tomorrow = data['daily'][1]  # [0]=今天 [1]=明天
    return {
        "fxDate": tomorrow['fxDate'],
        "moonPhase": tomorrow['moonPhase'],
        "tempMax": tomorrow['tempMax'],
        "tempMin": tomorrow['tempMin'],
        "textDay": tomorrow['textDay'],
        "textNight": tomorrow['textNight'],
        "windScaleDay": tomorrow['windScaleDay'],
        "uvIndex": tomorrow['uvIndex'],
        "humidity": tomorrow['humidity'],
    }

# ==================== 纪念日计算 ====================
def get_love_days():
    start = datetime.strptime(START_DATE, "%Y-%m-%d %H:%M:%S")
    delta = get_beijing_now() - start.replace(tzinfo=BEIJING_TZ)
    return str(delta.days)

def get_meet_days():
    meet = datetime.strptime(MEET_DATE, "%Y-%m-%d %H:%M:%S")
    delta = get_beijing_now() - meet.replace(tzinfo=BEIJING_TZ)
    return f"{delta.days}天"

# ==================== 生日倒计时 ====================
def get_birthday_left():
    today = get_beijing_now()
    try:
        next_birthday = datetime.strptime(f"{today.year}-{BIRTHDAY}", "%Y-%m-%d")
    except ValueError:
        next_birthday = datetime.strptime(f"{today.year}-02-28", "%Y-%m-%d")
    next_birthday = next_birthday.replace(tzinfo=BEIJING_TZ)
    if next_birthday < today:
        next_birthday = next_birthday.replace(year=next_birthday.year + 1)
    return (next_birthday - today).days

# ==================== 情话 ====================
def get_words(max_retries=3):
    for i in range(max_retries):
        try:
            resp = requests.get("https://api.shadiao.pro/chp", timeout=5)
            if resp.status_code == 200:
                return resp.json()['data']['text']
        except Exception:
            pass
        time.sleep(1)
    return "今天也要开心哦！"

# ==================== 贴心提示 ====================
def get_tips(text_day, text_night, temp_max, humidity, uv_index):
    tips = []
    temp = int(temp_max)
    humi = int(humidity)
    uv = int(uv_index)
    
    if '雨' in text_day or '雨' in text_night:
        tips.append('宝宝，明天有雨哦，记得带伞，小心着凉')
    else:
        if temp > 24:
            tips.append('宝宝，明天很暖和哦')
        elif 15 <= temp <= 24:
            tips.append('宝宝，明天很舒适哦')
        elif 10 <= temp < 15:
            tips.append('宝宝，明天可能有点冷，多穿点衣服')
        else:
            tips.append('宝宝，明天很冷，直接上羽绒服')
    
    if humi <= 40:
        tips.append('宝宝，明天空气很干，记得随身携带保湿产品')
    elif 40 < humi <= 50:
        tips.append('宝宝，明天空气偏干，记得涂点保湿的再出门')
    elif 50 < humi <= 70:
        tips.append('宝宝，明天空气适中，可以根据个人情况保湿')
    else:
        tips.append('宝宝，明天空气很润，保湿可以随意')
    
    if uv <= 2:
        tips.append('宝宝，明天紫外线很弱，大胆出门')
    elif 3 <= uv <= 4:
        tips.append('宝宝，明天紫外线偏弱，不用担心')
    elif 5 <= uv <= 6:
        tips.append('宝宝，明天紫外线较强，注意防晒')
    elif 7 <= uv <= 9:
        tips.append('宝宝，明天紫外线很强，可以防晒霜+伞走起')
    else:
        tips.append('宝宝，明天紫外线超强，需要防晒武装到牙齿了')
    
    return tips

# ==================== 随机颜色 ====================
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)

# ==================== 发送消息 ====================
def send_message(user_id, template_id, data):
    client = WeChatClient(APP_ID, APP_SECRET)
    wm = WeChatMessage(client)
    res = wm.send_template(user_id, template_id, data)
    print(f"发送给 {user_id} 成功: {res}")

# ==================== 主逻辑 ====================
def main():
    # 1. 天气
    weather = get_weather(CITY_CODE)
    
    # 2. 纪念日
    love_days = get_love_days()
    meet_days = get_meet_days()
    birthday_left = get_birthday_left()
    
    # 3. 情话
    love_words = get_words()
    
    # 4. 贴心提示
    tips = get_tips(
        weather['textDay'],
        weather['textNight'],
        weather['tempMax'],
        weather['humidity'],
        weather['uvIndex']
    )
    while len(tips) < 3:
        tips.append("宝宝，今天也要加油哦！")
    
    # 5. 组装模板数据
    data = {
        "love_days": {"value": love_days},
        "meet_days": {"value": meet_days},
        "birthday_left": {"value": birthday_left},
        "city": {"value": "广州市黄埔区"},
        "fxDate": {"value": weather['fxDate']},
        "moonPhase": {"value": weather['moonPhase']},
        "tempMax": {"value": weather['tempMax']},
        "tempMin": {"value": weather['tempMin']},
        "textDay": {"value": weather['textDay']},
        "textNight": {"value": weather['textNight']},
        "windScaleDay": {"value": weather['windScaleDay']},
        "uvIndex": {"value": weather['uvIndex']},
        "humidity": {"value": weather['humidity']},
        "tips0": {"value": tips[0]},
        "tips1": {"value": tips[1]},
        "tips2": {"value": tips[2]},
        "love_words": {"value": love_words},
        "color": {"value": get_random_color()},
    }
    
    # 6. 发送
    send_message(USER_ID1, TEMPLATE_ID, data)
    send_message(USER_ID2, TEMPLATE_ID, data)
    print("✅ 全部发送完成")

if __name__ == "__main__":
    main()
