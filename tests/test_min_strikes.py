import pytest


def test_set_min_strikes_5(as3935):
    as3935.set_min_strikes(5)
    assert (as3935.registers[0x02] & 0x30) == 0x10


def test_get_min_strikes_5(as3935):
    min_strikes = as3935.get_min_strikes()
    assert min_strikes == 5


def test_set_invalid_min_strikes(as3935):
    with pytest.raises(Exception):
        as3935.set_min_strikes(2)


def test_set_min_strikes_9(as3935):
    as3935.set_min_strikes(9)
    assert (as3935.registers[0x02] & 0x30) == 0x20


def test_get_min_strikes_9(as3935):
    min_strikes = as3935.get_min_strikes()
    assert min_strikes == 9


def test_set_min_strikes_16(as3935):
    as3935.set_min_strikes(16)
    assert (as3935.registers[0x02] & 0x30) == 0x30


def test_get_min_strikes_16(as3935):
    min_strikes = as3935.get_min_strikes()
    assert min_strikes == 16


def test_set_min_strikes_1(as3935):
    as3935.set_min_strikes(1)
    assert (as3935.registers[0x02] & 0x30) == 0x00


def test_get_min_strikes_1(as3935):
    min_strikes = as3935.get_min_strikes()
    assert min_strikes == 1
