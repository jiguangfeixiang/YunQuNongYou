# 这里的cron的定时任务
import datetime
import random
import time
from decimal import Decimal

import requests

from trip.models import GrowRecord, OwnedCrop

COLOR_CHOICES = {
    'green': '绿色',
    'yellow': '黄色',
    'red': '红色',
    'blue': '蓝色',
    'black': '黑色',
    'white': '白色'
}

PEST_STATUS_CHOICES = (
    ('healthy', '健康'),
    ('poisonous', '少量害虫骚扰'),
    ('dangerous', '危险'),
    ('dead', '死亡'),
    ('unknown', '未知'),
)


def assign_color_to_weather(weather):
    if weather == '晴':
        return 'green'
    elif weather == '阴':
        return 'yellow'
    elif weather == '雨':
        return 'blue'
    elif weather == '雪':
        return 'white'
    else:
        return 'black'


def assign_color_to_temperature(temp):
    temp = int(temp)
    if temp < 0:
        return 'blue'
    elif temp < 15:
        return 'yellow'
    elif temp < 30:
        return 'green'
    else:
        return COLOR_CHOICES['red']


def assign_color_to_humidity(hum):
    hum = int(hum)
    if hum < 30:
        return 'yellow'
    elif hum < 60:
        return 'green'
    else:
        return 'blue'


def assign_color_to_soil_ph(ph):
    ph = int(ph)
    if ph < 5:
        return 'red'
    elif ph <= 7:
        return 'green'
    else:
        return 'yellow'


def assign_color_to_co2_level(co2):
    co2 = int(co2)
    if co2 >= 10:
        return 'green'
    elif co2 <= 15:
        return 'yellow'
    else:
        return 'black'


def weather_url(city):
    return 'https://restapi.amap.com/v3/weather/weatherInfo?city={}&key=e145d010b4234ae436ebc43830c1f1ad'.format(city)


def weather_data(city):
    url = weather_url(city)
    # 发送请求
    response = requests.get(url)
    data = response.json()
    return data


def cron():
    print('cron的定时任务开启成功')


# 每天每10秒调用一次接口用来更新当天记录的基本信息
def update_record_info(times=10, date=None):
    while True:
        try:
            today_records = GrowRecord.objects.filter(record_date=datetime.date.today())  # 今天的所有记录
        except:
            print('未能获取到今天的记录')
            continue
        for record in today_records:
            # 获取这条记录作物的城市名字
            scene_city_name = record.owned_crop.crop_info.city
            data = weather_data(scene_city_name)
            count = data['count']
            print(data)
            if count != 0:
                # 更新记录的基本信息
                # 检查 'lives' 列表是否为空
                try:
                    info = data['lives'][0]
                except IndexError as e:
                    print(f"lives里没有数据哦.{e}")
                    continue
                weather = info['weather']
                temperature = info['temperature']
                humidity = info['humidity']
                soil_ph = round(random.uniform(4, 8.5), 2)
                pest_status = random.choice(PEST_STATUS_CHOICES)[0]
                co2_level = round(random.uniform(10, 20), 2)
                temperature_color = assign_color_to_temperature(temperature)
                humidity_color = assign_color_to_humidity(humidity)
                soil_ph_color = assign_color_to_soil_ph(soil_ph)
                co2_level_color = assign_color_to_co2_level(co2_level)
                # 进行保存操作
                today_records.update(weather=weather, temperature=temperature, temperature_color=temperature_color,
                                     air_humidity=humidity, air_humidity_color=humidity_color, soil_ph=soil_ph,
                                     soil_ph_color=soil_ph_color, pest_status=pest_status,
                                     co2_level=co2_level, co2_level_color=co2_level_color)
            else:
                print('未能获取到天气数据')
        time.sleep(times)


# 每天0点给拥有作物创建一条记录

def create_record(times=None):
    while True:
        current_time = datetime.datetime.now()
        # 检查是否是午夜或是否有外部触发
        if current_time.strftime('%H:%M:%S') == '00:00:00' or times:
            owned_crops = OwnedCrop.objects.all()
            for owned_crop in owned_crops:
                today_date = current_time.date()
                if not GrowRecord.objects.filter(record_date=today_date, owned_crop=owned_crop).exists():
                    record = GrowRecord.objects.create(record_date=today_date, owned_crop=owned_crop)
                    # 尝试获取前一天的记录
                    last_record, created = GrowRecord.objects.get_or_create(
                        record_date=today_date - datetime.timedelta(days=1),
                        defaults={'growth_height': 0,
                                  'growth_speed': 0},
                        owned_crop=owned_crop)

                    # 如果记录是新创建的，使用默认值
                    if created:
                        last_record.growth_height = 0
                        last_record.growth_speed = 0
                        last_record.save()

                    # 添加随机增长
                    record.growth_height = last_record.growth_height + Decimal(random.uniform(0.01, 0.5))
                    record.growth_speed = last_record.growth_speed + Decimal(random.uniform(0.01, 0.5))
                    record.save()
                else:
                    print(f'{owned_crop.crop_info.name}今日记录已存在，无需再次创建')

            times = None
            print(f'创建成功,接下来等到明天午夜')
        else:
            # 计算从现在到午夜的时间
            midnight = datetime.datetime.combine(current_time + datetime.timedelta(days=1),
                                                 datetime.datetime.min.time())
            seconds_until_midnight = (midnight - current_time).total_seconds()
            print(f'等待记录创建中，将在 {seconds_until_midnight} 秒后尝试')
            time.sleep(seconds_until_midnight)
