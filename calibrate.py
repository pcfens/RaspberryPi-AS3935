#!/usr/bin/env python
from RPi_AS3935 import RPi_AS3935

import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)

# Rev. 1 Raspberry Pis should leave bus set at 0, while rev. 2 Pis should set
# bus equal to 1. The address should be changed to match the address of the
# sensor. (Common implementations are in README.md)
sensor = RPi_AS3935(address=0x03, bus=1)


print "set indoors"
sensor.set_indoors(True)
print "set noise floor to 0"
sensor.set_noise_floor(0)

sensor.read_data()
print sensor.registers[0x08]


print "set register to get resonant frequency"
#set register to get resonant frequency
# NB: multiple reading by 16
sensor.set_disp_lco(True)
print "!! Measure IRQ for freq (x16)"

sensor.read_data()
print sensor.registers[0x08]


print "set tune cap, 5 second intervals (measure)"
for x in range(0, 16):
	print x
	sensor.calibrate(tun_cap=x)
	time.sleep(5.0)




time.sleep(5.0)
print "Reset IRQ for no freq output"   
#01111111 = 0x7F
sensor.set_disp_lco(False)

