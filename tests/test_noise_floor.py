def test_get_noise_floor(as3935):
    noise_floor = as3935.get_noise_floor()
    assert noise_floor == 0


def test_set_noise_floor(as3935):
    as3935.set_noise_floor(2)
    assert (as3935.registers[0x01] & 0x70) == 0x20


def test_raise_noise_floor(as3935):
    as3935.raise_noise_floor()
    assert (as3935.registers[0x01] & 0x70) == 0x30


def test_lower_noise_floor(as3935):
    as3935.lower_noise_floor()
    assert (as3935.registers[0x01] & 0x70) == 0x20
