RaspberryPi-AS3935
==================

A python library and demo script for interacting with the
[AMS Franklin Lightning Sensor][http://www.ams.com/eng/Products/RF-Products/Lightning-Sensor/AS3935].

This script will only work if the correct kernel modules are loaded
on your Pi.  Adafruit has a nice tutorial set up, though depending on
the breakout board that you use, you may not see anything show up when
you run `i2cdetect`.


## Breakout Board

The AS3935 is a small chip, and rather than trying to solder it myself
I purchased a (v2) breakout board from [Embedded Adventures][http://www.embeddedadventures.com/as3935_lightning_sensor_module_mod-1016.html].


## Connecting the AS3935

In my test setup I connected my breakout board to the Pi as shown

| AS3935 Pin | Raspberry Pi Pin |
| ---------: | :--------------- |
| 4 (GND)    | 25 (Ground)      |
| 5 (VDD)    | 1 (3v3 Power)    |
| 10 (IRQ)   | 17 (GPIO)        |
| 11 (I2CL)  | 5 (SCL)          |
| 13 (I2CD)  | 3 (SDA)          |

## Known Issues

### Addressing 

You may need edit line 6 of lightning.py so that the correct address is read.

| Breakout Board | Default Address |
| :------------- | :-------------- |
| Embedded Adeventures v2 | 0x00 |
| Embedded Adeventures v4 | 0x03 |
| Tautic Electronics | 0x00 |

### RaspberryPi Model

If you have one of the newer 512MB Pi boards, then you need to adjust line 6
to read
```python
sensor = AS3935(address = 0x00, bus = 1)
```
