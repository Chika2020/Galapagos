import requests
import json

def getEmonpiData():
	response = requests.get('http://10.132.88.132/feed/fetch.json?ids=1,2,3',headers={'Authorization': 'd24eb23067bf7eefaf7e3489837e36c8'})
	print(response.json())
	d = response.json()
	voltage = d[0]
	power = d[1]
	print(voltage)
	print(power)
	return d
