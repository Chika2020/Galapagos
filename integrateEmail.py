import MySQLdb
from datetime import datetime
import time
import PCF8591 as ADC
import RPi.GPIO as GPIO
import math

# database scrap imports
import csv
import pandas as pd
from emailCSV import sendEmail

DO = 17
GPIO.setmode(GPIO.BCM)
def setup():
	ADC.setup(0x48)
	GPIO.setup(DO, GPIO.IN)


def func():
	status = 1
	tmp = 1
	analogVal = ADC.read(0)
	Vr = 5 * float(analogVal) / 255
	Rt = 10000 * Vr / (5 - Vr)
	temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
	temp = temp - 273.15
	#print (temp)
	return int(temp)
# print(datetime.now().time()) --meant for testing, removeable

myDateObj = datetime.now()
timestampy = myDateObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")


setup()
temp = func()

db = MySQLdb.connect("localhost", "admin", "password", "temps")
curs = db.cursor()

sql = """INSERT INTO demotable (DateNTime,tempDat, otherVal, anotherVal, oneVal)
	 VALUES (%s, %s, %s, %s, %s)"""
#  ('dateY',  otherVal, anotherVal, oneVal)"""
val = (timestampy, temp, temp, temp, temp)

curs.execute(sql,val) #removed val
db.commit()

def DBscrape(query):
	df = pd.read_sql(query, con=db)
	df.to_csv("Output.csv",index=False)

	sendEmail("Output.csv")
	curs.execute(query)
	row = curs.fetchone()
	db.close()
q1 = "SELECT * FROM demotable"
DBscrape(q1)
