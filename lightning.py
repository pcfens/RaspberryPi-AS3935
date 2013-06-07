from AS3935 import AS3935
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
sensor = AS3935(address = 0x00, bus = 0)

sensor.calibrate()
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
        print "It was " + distance + "km away."

pin = 17
GPIO.setup(pin, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.add_event_detect(pin, GPIO.RISING, callback=handle_interrupt)

try: 
    print "Waiting for lightning - or at least something that looks like it"
    GPIO.wait_for_edge(24, GPIO.FALLING)

except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  

GPIO.cleanup()           # clean up GPIO on normal exit  
