from AS3935 import AS3935
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
sensor = AS3935(address = 0x00, bus = 0)

sensor.calibrate()
sensor.set_indoors(1)

def handle_interrupt():
    global sensor
    time.sleep(0.003)
    reason = sensor.get_interrupt()
    if reason == 0x01:
        print "Noise level too high - adjusting"
        floor = sensor.get_noise_floor()
        if floor < 7:
            floor = floor + 1
            sensor.set_noise_floor(floor)
        else:
            print "Noise floor is already at max"
    elif reason == 0x04:
        print "Disturber detected - masking"
        sensor.set_mask_disturber(1)
    elif reason == 0x08:
        distance = sensor.get_distance()
        print "We sensed lightning!"
        print "It was " + distance + "km away."

def falling_edge():
    print "Interrupt cleared"


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
