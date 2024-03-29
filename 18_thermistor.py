#!/usr/bin/env python3
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math

DO = 17
GPIO.setmode(GPIO.BCM)


def voltageMon():
	while(1):
		aVal = ADC.read(0)
		V = 5 * float(aVal) / 255
		print("Voltage:", V)

def setup():
	ADC.setup(0x48)
	GPIO.setup(DO, GPIO.IN)

	
def loop():
	status = 1
	tmp = 1
	
	analogVal = ADC.read(0) #should be ground -Yeray
	Vr = 5 * float(analogVal) / 255
	print("Voltage 2",Vr)
	Rt = 10000 * Vr / (5 - Vr)
	temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
	temp = temp - 273.15
	print ('temperature', temp)
        print ('voltage 2',Vr)

if __name__ == '__main__':
	try:
		setup()
		#voltageMon()
		loop()
	except KeyboardInterrupt: 
		pass	
