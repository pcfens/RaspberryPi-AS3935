def test_set_mask_disturber(as3935):
    as3935.set_mask_disturber(True)
    assert (as3935.registers[0x03] & 0x20) == 0x20
