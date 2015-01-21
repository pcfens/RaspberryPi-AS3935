def test_set_disp_lco_true(as3935):
    as3935.set_disp_lco(True)
    assert (as3935.registers[0x08] & 0x80) == 0x80


def test_get_disp_lco_true(as3935):
    disp_lco = as3935.get_disp_lco()
    assert disp_lco is True


def test_set_disp_lco_false(as3935):
    as3935.set_disp_lco(False)
    assert (as3935.registers[0x08] & 0x80) == 0x00


def test_get_disp_lco_false(as3935):
    disp_lco = as3935.get_disp_lco()
    assert disp_lco is False
