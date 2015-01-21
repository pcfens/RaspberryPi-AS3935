import time


class RPi_AS3935:
    """A basic class used for interacting with the AS3935 lightning
    sensor from a Raspberry Pi over I2C"""

    def __init__(self, address, bus=0):
        self.address = address
        import smbus
        self.i2cbus = smbus.SMBus(bus)

    def calibrate(self, tun_cap=None):
        """Calibrate the lightning sensor - this takes up to half a second
        and is blocking.

        The value of tun_cap should be between 0 and 15, and is used to set
        the internal tuning capacitors (0-120pF in steps of 8pF)
        """
        time.sleep(0.08)
        self.read_data()
        if tun_cap is not None:
            if tun_cap < 0x10 and tun_cap > -1:
                self.set_byte(0x08, (self.registers[0x08] & 0xF0) | tun_cap)
                time.sleep(0.002)
            else:
                raise Exception("Value of TUN_CAP must be between 0 and 15")
        self.set_byte(0x3D, 0x96)
        time.sleep(0.002)
        self.set_byte(0x08, self.registers[0x08] | 0x20)
        time.sleep(0.002)
        self.read_data()
        self.set_byte(0x08, self.registers[0x08] & 0xDF)
        time.sleep(0.002)

    def reset(self):
        """Reset all registers to their default power on values
        """
        self.set_byte(0x3C, 0x96)

    def get_interrupt(self):
        """Get the value of the interrupt register

        0x01 - Too much noise
        0x04 - Disturber
        0x08 - Lightning
        """
        self.read_data()
        return self.registers[0x03] & 0x0F

    def get_distance(self):
        """Get the estimated distance of the most recent lightning event
        """
        self.read_data()
        if self.registers[0x07] & 0x3F == 0x3F:
            return False
        else:
            return self.registers[0x07] & 0x3F

    def get_noise_floor(self):
        """Get the noise floor value.

        Actual voltage levels used in the sensor are located in Table 16
        of the data sheet.
        """
        self.read_data()
        return (self.registers[0x01] & 0x70) >> 4

    def set_noise_floor(self, noisefloor):
        """Set the noise floor value.

        Actual voltage levels used in the sensor are located in Table 16
        of the data sheet.
        """
        self.read_data()
        noisefloor = (noisefloor & 0x07) << 4
        write_data = (self.registers[0x01] & 0x8F) + noisefloor
        self.set_byte(0x01, write_data)

    def lower_noise_floor(self, min_noise=0):
        """Lower the noise floor by one step.

        min_noise is the minimum step that the noise_floor should be
        lowered to.
        """
        floor = self.get_noise_floor()
        if floor > min_noise:
            floor = floor - 1
            self.set_noise_floor(floor)
        return floor

    def raise_noise_floor(self, max_noise=7):
        """Raise the noise floor by one step

        max_noise is the maximum step that the noise_floor should be
        raised to.
        """
        floor = self.get_noise_floor()
        if floor < max_noise:
            floor = floor + 1
            self.set_noise_floor(floor)
        return floor

    def get_min_strikes(self):
        """Get the number of lightning detections required before an
        interrupt is raised.
        """
        self.read_data()
        value = (self.registers[0x02] >> 4) & 0x03
        if value == 0:
            return 1
        elif value == 1:
            return 5
        elif value == 2:
            return 9
        elif value == 3:
            return 16

    def set_min_strikes(self, minstrikes):
        """Set the number of lightning detections required before an
        interrupt is raised.

        Valid values are 1, 5, 9, and 16, any other raises an exception.
        """
        if minstrikes == 1:
            minstrikes = 0
        elif minstrikes == 5:
            minstrikes = 1
        elif minstrikes == 9:
            minstrikes = 2
        elif minstrikes == 16:
            minstrikes = 3
        else:
            raise Exception("Value must be 1, 5, 9, or 16")

        self.read_data()
        minstrikes = (minstrikes & 0x03) << 4
        write_data = (self.registers[0x02] & 0xCF) + minstrikes
        self.set_byte(0x02, write_data)

    def get_indoors(self):
        """Determine whether or not the sensor is configured for indoor
        use or not.

        Returns True if configured to be indoors, otherwise False.
        """
        self.read_data()
        if self.registers[0x00] & 0x10 == 0x10:
            return True
        else:
            return False

    def set_indoors(self, indoors):
        """Set whether or not the sensor should use an indoor configuration.
        """
        self.read_data()
        if indoors:
            write_value = (self.registers[0x00] & 0xE0) + 0x12
        else:
            write_value = (self.registers[0x00] & 0xE0) + 0x0E
        self.set_byte(0x00, write_value)

    def set_mask_disturber(self, mask_dist):
        """Set whether or not disturbers should be masked (no interrupts for
        what the sensor determines are man-made events)
        """
        self.read_data()
        if mask_dist:
            write_value = self.registers[0x03] | 0x20
        else:
            write_value = self.registers[0x03] & 0xDF
        self.set_byte(0x03, write_value)

    def get_mask_disturber(self):
        """Get whether or not disturbers are masked or not.

        Returns True if interrupts are masked, false otherwise
        """
        self.read_data()
        if self.registers[0x03] & 0x20 == 0x20:
            return True
        else:
            return False

    def set_disp_lco(self, display_lco):
        """Have the internal LC oscillator signal displayed on the interrupt pin for
        measurement.

        Passing display_lco=True enables the output, False disables it.
        """
        self.read_data()
        if display_lco:
            self.set_byte(0x08, (self.registers[0x08] | 0x80))
        else:
            self.set_byte(0x08, (self.registers[0x08] & 0x7F))
        time.sleep(0.002)

    def get_disp_lco(self):
        """Determine whether or not the internal LC oscillator is displayed on the
        interrupt pin.

        Returns True if the LC oscillator is being displayed on the interrupt pin,
        False otherwise
        """
        self.read_data()
        if self.registers[0x08] & 0x80 == 0x80:
            return True
        else:
            return False

    def set_byte(self, register, value):
        """Write a byte to a particular address on the sensor.

        This method should rarely be used directly.
        """
        self.i2cbus.write_byte_data(self.address, register, value)

    def read_data(self):
        """
        Read a block of data from the sensor and store it.

        This doesn't read exact registers because the library used by
        smbus doesn't support repeated I2C starts (required to read
        registers directly on the sensor)

        This method should rarely be called directly.
        """
        self.registers = self.i2cbus.read_i2c_block_data(self.address, 0x00)
