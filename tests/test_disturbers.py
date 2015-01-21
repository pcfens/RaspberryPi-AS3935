def test_set_mask_disturber_true(as3935):
    as3935.set_mask_disturber(True)
    assert (as3935.registers[0x03] & 0x20) == 0x20


def test_get_mask_disturber_true(as3935):
    mask_disturber = as3935.get_mask_disturber()
    assert mask_disturber is True


def test_set_mask_disturber_false(as3935):
    as3935.set_mask_disturber(False)
    assert (as3935.registers[0x03] & 0x20) == 0x00


def test_get_mask_disturber_false(as3935):
    mask_disturber = as3935.get_mask_disturber()
    assert mask_disturber is False
