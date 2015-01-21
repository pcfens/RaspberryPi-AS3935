def test_set_indoors_true(as3935):
    as3935.set_indoors(True)
    assert (as3935.registers[0x00] & 0x10) == 0x10


def test_get_indoors_true(as3935):
    indoors = as3935.get_indoors()
    assert indoors is True


def test_set_indoors_false(as3935):
    as3935.set_indoors(False)
    assert (as3935.registers[0x00] & 0x10) == 0x00


def test_get_indoors_false(as3935):
    indoors = as3935.get_indoors()
    assert indoors is False
