import requests
import json
response = requests.get('http://153.104.46.244/feed/fetch.json?ids=1,2,3',headers={'Authorization': 'd24eb23067bf7eefaf7e3489837e36c8'})
print(response.json())
d = response.json()
voltage = d[0]
current = d[1]

