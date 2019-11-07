# need help with making sure that my integration is 
# at least somewhat ok, commented where I added lines
# Goal: Get loop function to return temp and have that placed into DB
# just once!
# Must fix (OG): Data gets added to DB once, then NULL data is added in second
# row
# do I want my work inside a function and have that be called instead?
# 11/4/19 DOES NOT RUN, HAS NOT BE RAN

import MySQLdb
from datetime import datetime
import time
import PCF8591 as ADC
import RPi.GPIO as GPIO
import math

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
	return int(temp) # added this - CT 11/4/19

dateY = time.strftime('%Y/%m/%d %H:%M:%S')

# print(dateY)
# value = loop()
# valueT = 14
# valueTh = 13
# valueF = 12
setup()
temp = func()

db = MySQLdb.connect("localhost", "admin", "password", "temps")
curs = db.cursor()

sql = """INSERT INTO integrate (tempDate, tempDat, otherVal, anotherVal, oneVal)
	 VALUES (%s, %s, %s, %s, %s)"""
#  ('dateY', tempDat, otherVal, anotherVal, oneVal)"""
val = (dateY, temp, temp, temp, temp)

curs.execute(sql,val) #removed val
db.commit()
