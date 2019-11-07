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
        while True:
                analogVal = ADC.read(0)
                Vr = 5 * float(analogVal) / 255
                vin = Vr/(465)
                Area = 50.8* 50.8 / (100*100)
                Power = pow(vin, 2) /465
                Radiation = Power / Area
                print(vin)
                print(Radiation)
