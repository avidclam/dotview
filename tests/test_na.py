import copy

from dotview.na import NA, NAType


def test_na_is_singleton():
    assert NA is NAType()
    assert NA is NAType()


def test_na_repr_and_str():
    assert repr(NA) == "<NA>"
    assert str(NA) == "<NA>"


def test_na_bool_is_false():
    assert bool(NA) is False


def test_na_comparisons_propagate():
    assert (NA == 1) is NA
    assert (NA != 1) is NA
    assert (NA < 1) is NA
    assert (NA <= 1) is NA
    assert (NA > 1) is NA
    assert (NA >= 1) is NA


def test_na_arithmetic_propagates():
    assert (NA + 1) is NA
    assert (1 + NA) is NA
    assert (NA - 1) is NA
    assert (1 - NA) is NA
    assert (NA * 2) is NA
    assert (2 * NA) is NA
    assert (NA / 2) is NA
    assert (2 / NA) is NA
    assert (NA // 2) is NA
    assert (2 // NA) is NA
    assert (NA % 2) is NA
    assert (2 % NA) is NA
    assert (NA ** 2) is NA
    assert (2 ** NA) is NA
    assert (-NA) is NA
    assert (+NA) is NA
    assert abs(NA) is NA


def test_na_copy_and_deepcopy_return_singleton():
    assert copy.copy(NA) is NA
    assert copy.deepcopy(NA) is NA
