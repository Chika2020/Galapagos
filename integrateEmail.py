import MySQLdb
from datetime import datetime
import time
import PCF8591 as ADC
import RPi.GPIO as GPIO
import math

# database scrape imports
import csv
import pandas as pd
from emailCSV import sendEmail

# EmonPi Data imports
from request import getEmonpiData
import json

# insolation imports
from insolarxtemp import insolar

# CT imports
from ctTryAgain import ctFunc

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
temp = func() # temp function call
voltPower = getEmonpiData() # emonpi function call
insolData = insolar() # insolation function call
ctData = ctFunc() # CT function call
print(ctData)

voltData = voltPower[0]
powData = voltPower[1]

db = MySQLdb.connect("localhost", "admin", "password", "temps")
curs = db.cursor()

sql = """INSERT INTO demotable (DateNTime,tempData, voltageData, powerData, insolationData, ctData)
	 VALUES (%s, %s, %s, %s, %s, %s)"""

val = (timestampy, temp, voltData, powData, insolData, ctData) #replace second insol with CT

curs.execute(sql,val)
db.commit()

def DBscrape(query):
	df = pd.read_sql(query, con=db)
	df.to_csv("WeeklyReport.csv",index=False)

	sendEmail("WeeklyReport.csv")
	curs.execute(query)
	row = curs.fetchone()
	db.close()
q1 = "SELECT * FROM demotable"
DBscrape(q1)
