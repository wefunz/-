import requests
import pprint
import re
import pymysql
import time
import datetime
import json
import demjson
import pprint

import numpy as np
np.set_printoptions(threshold = 1e6)
# C:\Users\zwf\Desktop\2020-2-10 2325.txt
with open(r"F:\\曾伟峰\\新建文本文档.txt",'r',encoding='utf-8') as f:
    datas = f.read()

    json_data = json.loads(datas)
    pprint.pprint(json_data)
    datas=json_data['data']['areaTree']
    conn = pymysql.connect("localhost", "root", "123456", "feiyan", charset='utf8')

    country_name = []
    province_name = []
    city_name = []
    city_id = []
    today_confirm = []
    today_suspect = []
    today_heal = []
    today_dead = []
    total_confirm = []
    total_dead = []
    total_suspect = []
    total_heal = []
    time = []
    summ = [country_name, province_name, city_name, city_id, today_confirm, today_dead, today_suspect, today_heal,
            total_confirm, total_dead, total_suspect, total_heal,time]
    for data in datas:
        if data['children']:
            guojia = data['children']
            for province in guojia:
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
            time.append(city['lastUpdateTime'])

    shuzus = np.transpose(summ)
    for i in range(len(shuzus)):
        for j in range(len(shuzus[0])):
            if shuzus[i][j] == None:
                shuzus[i][j] = 0
    print(shuzus)
    for shuzu in shuzus:
        sql = "insert into feb_26th (area_id,country_name,province_name,city_name,today_confirm,today_dead,today_suspect,today_heal,total_confirm,total_dead,total_suspect,total_heal,update_time) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(
            shuzu[3],shuzu[0], shuzu[1], shuzu[2],shuzu[4], shuzu[5], shuzu[6], shuzu[7],
            shuzu[8], shuzu[9], shuzu[10], shuzu[11], shuzu[12])
        try:
            conn.query(sql)
            conn.commit()


        except Exception as e:
            print(e)
            pass
            conn.close()
