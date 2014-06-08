from RPi_AS3935 import RPi_AS3935

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# note: bus must be '0' for the older 256MB raspberry pi's while the newer 512MB should have bus=1
# address must be 0x03 for the V4 of the MOD-1016
sensor = RPi_AS3935(address=0x00, bus=0)

sensor.calibrate(tun_cap=0x0F)
sensor.set_indoors(True)
sensor.set_noise_floor(0)

def handle_interrupt(channel):
    time.sleep(0.003)
    global sensor
    reason = sensor.get_interrupt()
    if reason == 0x01:
        print "Noise level too high - adjusting"
        sensor.raise_noise_floor()
    elif reason == 0x04:
        print "Disturber detected - masking"
        sensor.set_mask_disturber(True)
    elif reason == 0x08:
        distance = sensor.get_distance()
        print "We sensed lightning!"
        print "It was " + str(distance) + "km away."

pin = 17

GPIO.setup(pin, GPIO.IN)
GPIO.add_event_detect(pin, GPIO.RISING, callback=handle_interrupt)

print "Waiting for lightning - or at least something that looks like it"

while True:
    time.sleep(1.0)
