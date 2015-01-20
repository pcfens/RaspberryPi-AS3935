from RPi_AS3935 import RPi_AS3935
import pytest


class RPi_AS3935Proxy(RPi_AS3935):
    def __init__(self, address, bus=0):
        self.address = address
        self.i2cbus = bus
        self.registers = [50, 2, 194, 32, 0, 0, 0, 63, 0, 173, 0, 37, 3, 1, 34, 131, 1, 31, 67, 2, 27, 99, 3, 24, 20, 5, 20, 157, 7, 17, 106, 11]

    def set_byte(self, register, value):
        self.registers[register] = value
        print value

    def read_data(self):
        self.registers = self.registers


@pytest.fixture(scope='module')
def as3935():
    return RPi_AS3935Proxy(address=0x00, bus=0)
