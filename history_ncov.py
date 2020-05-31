import requests
import pprint
import numpy as np
import json
import pymysql


headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}
url = 'http://ncov.nosensor.com:8080/api/'
response = requests.get(url,headers,timeout = 500)
conn = pymysql.connect("localhost", "root", "123456", "feiyan", charset='utf8' )
# print(response.text)
datas = json.loads(response.text)
datas = datas["city"]
Time = []
Province = []
City = []
Confirmed = []
Dead =[]
Cured =[]
Severe = []
Critical = []
all_datas = [Province,City,Confirmed,Dead,Cured,Severe,Critical,Time]
for data in datas:

    for province in data["CityDetail"]:
        Time.append(data["Time"])
        Province.append(province['Province'])
        City.append(province['City'])
        Confirmed.append(province['Confirmed'])
        Dead.append(province['Dead'])
        Cured.append(province['Cured'])
        Severe.append(province['Severe'])
        Critical.append(province['Critical'])

all_datas = np.transpose(all_datas)
i = 0
for all_data in all_datas:
    sql = "insert into history_ncov(province,city,confirmed,dead,cured,severe,critical,time) values ('{}','{}','{}','{}','{}','{}','{}','{}');".format(
        all_data[0],all_data[1],all_data[2],all_data[3],all_data[4],all_data[5],all_data[6],all_data[7])
    print("已经上传{}条数据".format(i))
    i = i+1
    try:
        conn.query(sql)
        conn.commit()




    except Exception as e:
        print(e)
        pass
        conn.close()

