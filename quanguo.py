import requests
import pprint
import re
import pymysql.cursors
import time
import datetime
import pprint

import numpy as np
np.set_printoptions(threshold = 1e6)
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}
url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=1581346031174'  # 疫情公告网站
html = requests.get(url,headers=headers)
datas = html.json()

datas = datas['data']
conn = pymysql.connect("localhost", "root", "123456", "feiyan", charset='utf8' )

cur = conn.cursor()
datas=datas['areaTree']

country_name = []
province_name = []
city_name = []
city_id = []
today_confirm = []
today_suspect = []
today_heal = []
today_dead =[]
total_confirm = []
total_dead = []
total_suspect = []
total_heal = []
time = []
summ = [country_name,province_name,city_name,city_id,today_confirm,today_dead,today_suspect,today_heal,total_confirm,total_dead,total_suspect,total_heal,time]
pprint.pprint(datas)
for data in datas:
    if data['children']:
        guojia=data['children']
        # pprint.pprint(data['id'])
        print("*******************")

        for province in guojia:
            if province['children']:
                for city in province['children']:
                    country_name.append(data['name'])
                    province_name.append(province['name'])
                    today_confirm.append(city['today']['confirm'])
                    today_suspect.append(city['today']['suspect'])
                    today_heal.append(city['today']['heal'])
                    today_dead.append(city['today']['dead'])
                    total_confirm.append(city['total']['confirm'])
                    total_suspect.append(city['total']['suspect'])
                    total_heal.append(city['total']['heal'])
                    total_dead.append(city['total']['dead'])
                    city_name.append(city['name'])
                    city_id.append(city['id'])
                    time.append(city['lastUpdateTime'])
            else:
                country_name.append(data['name'])
                province_name.append(province['name'])
                today_confirm.append(province['today']['confirm'])
                today_suspect.append(province['today']['suspect'])
                today_heal.append(province['today']['heal'])
                today_dead.append(province['today']['dead'])
                total_confirm.append(province['total']['confirm'])
                total_suspect.append(province['total']['suspect'])
                total_heal.append(province['total']['heal'])
                total_dead.append(province['total']['dead'])
                city_name.append(province['name'])
                city_id.append(province['id'])
                time.append(province['lastUpdateTime'])

    else:
        city_id.append(data['id'])
        country_name.append(data['name'])
        province_name.append('')
        city_name.append('')
        today_confirm.append(data['today']['confirm'])
        today_suspect.append(data['today']['suspect'])
        today_heal.append(data['today']['heal'])
        today_dead.append(data['today']['dead'])
        total_confirm.append(data['total']['confirm'])
        total_suspect.append(data['total']['suspect'])
        total_heal.append(data['total']['heal'])
        total_dead.append(data['total']['dead'])
        time.append(data['lastUpdateTime'])
shuzus=np.transpose(summ)
for i in range(len(shuzus)):
    for j in range(len(shuzus[0])):
        if shuzus[i][j] == None:
            shuzus[i][j] = 0
print(shuzus)
i=0
sql1="CREATE TABLE may_31th LIKE mar_22th"
try:
    cur.execute(sql1)
    conn.commit()
except Exception as e:
    print(e)
    pass

for shuzu in shuzus:
    if (str(shuzu[3])=='95XXXX'):
        shuzu[3]==0
    i=i+1
    sql2 = "insert into may_31th (area_id,country_name,province_name,city_name,today_confirm,today_dead,today_suspect,today_heal,total_confirm,total_dead,total_suspect,total_heal,update_time) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(
        shuzu[3],shuzu[0], shuzu[1], shuzu[2],shuzu[4], shuzu[5], shuzu[6], shuzu[7],
        shuzu[8], shuzu[9], shuzu[10], shuzu[11], shuzu[12])
    print("已经插入{}条数据".format(i))
    try:
        conn.query(sql2)
        conn.commit()


    except Exception as e:
        print(e)
        pass
        conn.close()









