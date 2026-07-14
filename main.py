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
START_DATE = os.getenv("START_DATE")            # 恋爱开始日期，格式：2024-09-22 00:00:00
MEET_DATE = os.getenv("MEET_DATE")              # 相遇日期，格式：2024-08-31 00:00:00
BIRTHDAY = os.getenv("BIRTHDAY")                # 生日，格式：03-12
CITY_CODE = os.getenv("CITY_CODE", "101280111") # 城市代码，默认广州黄埔

# ==================== 北京时间工具 ====================
BEIJING_TZ = timezone(timedelta(hours=8))

def get_beijing_now():
    """获取当前北京时间"""
    return datetime.now(BEIJING_TZ)

# ==================== 天气获取 ====================
def get_weather(city_code):
    """获取明天天气，返回列表"""
    url = f"https://devapi.qweather.com/v7/weather/3d?location={city_code}&key={WEATHER_KEY}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    
    # daily[0]=今天, daily[1]=明天
    tomorrow = data['daily'][1]
    
    return [
        tomorrow['fxDate'],        # 日期
        tomorrow['moonPhase'],     # 月相
        tomorrow['tempMax'],       # 最高温
        tomorrow['tempMin'],       # 最低温
        tomorrow['textDay'],       # 白天天气
        tomorrow['textNight'],     # 夜间天气
        tomorrow['windScaleDay'],  # 风力
        tomorrow['uvIndex'],       # 紫外线
        tomorrow['humidity'],      # 湿度
    ]

# ==================== 纪念日计算 ====================
def get_love_days():
    """计算恋爱天数"""
    start = datetime.strptime(START_DATE, "%Y-%m-%d %H:%M:%S")
    delta = get_beijing_now() - start.replace(tzinfo=BEIJING_TZ)
    return str(delta.days)

def get_meet_days():
    """计算相遇天数"""
    meet = datetime.strptime(MEET_DATE, "%Y-%m-%d %H:%M:%S")
    delta = get_beijing_now() - meet.replace(tzinfo=BEIJING_TZ)
    return f"{delta.days}天"

# ==================== 生日倒计时 ====================
def get_birthday_left():
    """计算距离下一个生日还有多少天"""
    today = get_beijing_now()
    try:
        next_birthday = datetime.strptime(f"{today.year}-{BIRTHDAY}", "%Y-%m-%d")
    except ValueError:
        # 如果今年没有 2月29日，按 2月28日 处理
        next_birthday = datetime.strptime(f"{today.year}-02-28", "%Y-%m-%d")
    
    next_birthday = next_birthday.replace(tzinfo=BEIJING_TZ)
    if next_birthday < today:
        next_birthday = next_birthday.replace(year=next_birthday.year + 1)
    
    return (next_birthday - today).days

# ==================== 土味情话 ====================
def get_words(max_retries=3):
    """获取土味情话，带有限重试"""
    for i in range(max_retries):
        try:
            resp = requests.get("https://api.shadiao.pro/chp", timeout=5)
            if resp.status_code == 200:
                return resp.json()['data']['text']
        except Exception:
            pass
        time.sleep(1)
    return "今天也要开心哦！"  # 降级文案

# ==================== 贴心小提示 ====================
def get_tips(weather_text_day, weather_text_night, temp_max, humidity, uv_index):
    """根据天气生成生活小贴士"""
    tips = []
    temp = int(temp_max)
    humi = int(humidity)
    uv = int(uv_index)
    
    # 雨天/晴天 穿衣建议
    if '雨' in weather_text_day or '雨' in weather_text_night:
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
    
    # 湿度建议
    if humi <= 40:
        tips.append('宝宝，明天空气很干，记得随身携带保湿产品')
    elif 40 < humi <= 50:
        tips.append('宝宝，明天空气偏干，记得涂点保湿的再出门')
    elif 50 < humi <= 70:
        tips.append('宝宝，明天空气适中，可以根据个人情况保湿')
    else:
        tips.append('宝宝，明天空气很润，保湿可以随意')
    
    # 紫外线建议
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
    # 1. 获取天气
    city_name = "广州市黄埔区"  # 可改成从环境变量读取
    weather_data = get_weather(CITY_CODE)
    fx_date, moon_phase, temp_max, temp_min, text_day, text_night, wind_scale, uv_index, humidity = weather_data
    
    # 2. 获取纪念日
    love_days = get_love_days()
    meet_days = get_meet_days()
    birthday_left = get_birthday_left()
    
    # 3. 获取情话
    love_words = get_words()
    
    # 4. 生成小贴士
    tips = get_tips(text_day, text_night, temp_max, humidity, uv_index)
    # 确保至少有3条，不足则补默认
    while len(tips) < 3:
        tips.append("宝宝，今天也要加油哦！")
    
    # 5. 组装模板数据
    data = {
        "love_days": {"value": love_days},
        "meet_days": {"value": meet_days},
        "birthday_left": {"value": birthday_left},
        "city": {"value": city_name},
        "fxDate": {"value": fx_date},
        "moonPhase": {"value": moon_phase},
        "tempMax": {"value": temp_max},
        "tempMin": {"value": temp_min},
        "textDay": {"value": text_day},
        "textNight": {"value": text_night},
        "windScaleDay": {"value": wind_scale},
        "uvIndex": {"value": uv_index},
        "humidity": {"value": humidity},
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
