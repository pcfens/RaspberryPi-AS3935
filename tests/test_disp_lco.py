def test_set_disp_lco(as3935):
    as3935.set_disp_lco(True)
    assert (as3935.registers[0x08] & 0x80) == 0x80
