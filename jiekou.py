import requests

url='http://lab.isaaclin.cn/nCoV/api/area?latest=0'
response= requests.get(url)
print(response.text)