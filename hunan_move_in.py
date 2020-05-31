import requests
import pprint
import re
import json
import numpy as np
import time,datetime
from datetime import timedelta
def datelist(start,end):
    date_list = []
    begin_date = datetime.datetime.strptime(start, r"%Y%m%d")
    end_date = datetime.datetime.strptime(end,r"%Y%m%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime(r"%Y%m%d")
        date_list.append(date_str)
        # 日期加法days=1 months=1等等
        begin_date += timedelta(days=1)
    return date_list


def time_shift(date_time):

    date_time= date_time[0:4]+"-"+date_time[4:6]+"-"+date_time[6:8]
    riqi= datetime.date(*map(int, date_time.split('-')))
    return riqi


dates = datelist('20200112','20200215')
for date in dates:
    print(date)
    url= 'https://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id=430000&type=move_in&date={}&callback=jsonp_1581748712277_8271303'.format(date)
    datas = requests.get(url)

    datas=datas.text.encode('utf-8').decode("unicode_escape")

    pattern = re.compile('.*?\((.*?)\)',re.S)
    datas =re.findall(pattern,datas)[0]
    datas= json.loads(datas)
    date_time = time_shift(date)
    print(date_time)
    datas = datas['data']['list']
    city_name = []
    province_name = []
    value = []
    riqi = []
    all_data = [city_name,province_name,value,riqi]
    for data in datas:
        city_name.append(data['city_name'])
        province_name.append(data['province_name'])
        value.append(data['value'])
        riqi.append(date_time)
    all_data = np.transpose(all_data)
    print('*********************')
    print(all_data)