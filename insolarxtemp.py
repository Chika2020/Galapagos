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

	
def temp():
	status = 1
	tmp = 1
	
	analogVal = ADC.read(0) #should be ground -Yeray
	Vr = 5 * float(analogVal) / 255
	Rt = 10000 * Vr / (5 - Vr)
	temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
	temp = temp - 273.15
	print ('temperature', temp)
        print ('voltage temp',Vr)


def insolar():
        status = 1
        tmp = 1
        analogVal = ADC.read(1)
        Vr = 5 * float(analogVal) / 255 # Should be 5V -Yeray

        Area = 50.8* 50.8 / (100*100)
        Power = pow(Vr, 2) /465
        Radiation = Power / Area
        print("solar cell voltage",Vr)
        print ("Insolation", Radiation)


if __name__ == '__main__':
	try:
		setup()
		#voltageMon()
		temp()
                insolar()
	except KeyboardInterrupt: 
		pass	
