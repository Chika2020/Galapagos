#!/usr/bin/env python3
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math

DO = 17
GPIO.setmode(GPIO.BCM)

def setup():
        ADC.setup(0x48)
        GPIO.setup(DO, GPIO.IN)


def loop():
        status = 1
        tmp = 1
        analogVal = ADC.read(2)
        Vr = 5 * float(analogVal) / 255

       # analogVal = ADC.read(1)
        #Vr = 5 * float(analogVal) / 255
        Area = 50.8* 50.8 / (100*100)
        Power = pow(Vr, 2) /465
        Radiation = Power / Area
        print(Vr)
        print(Radiation)


if __name__ == '__main__':
                setup()
                loop()

