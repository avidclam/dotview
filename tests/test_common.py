import pytest

from dotview.common import truncate, truncate_repr
import dotview.common as common
from dotview import config


def test_truncate_returns_full_string_when_max_len_none():
    result = truncate("abcdef", padding="...")
    assert result == "abcdef"


def test_truncate_returns_empty_string_when_max_len_zero():
    result = truncate("abcdef", padding="...", max_len=0)
    assert result == ""


def test_truncate_respects_max_len_and_padding():
    result = truncate("abcdef", padding="..", max_len=4)
    assert result == "ab.."


def test_truncate_chops_padding_when_max_len_below_padding_length():
    result = truncate("abcdef", padding="....", max_len=2)
    assert result == ".."


def test_truncate_no_change_when_short_enough():
    assert truncate("abc", padding="...", max_len=5) == "abc"


def test_truncate_repr_uses_config_max_by_default():
    class Sample:
        def __repr__(self):
            return "X" * (config.TRUNCATE_REPR_MAX_LEN + 10)

    result = truncate_repr(Sample())
    assert len(result) == config.TRUNCATE_REPR_MAX_LEN


def test_truncate_repr_enforces_min_len():
    class Sample:
        def __repr__(self):
            return "Y" * 50

    result = truncate_repr(Sample(), max_len=5)
    assert len(result) == config.TRUNCATE_REPR_MIN_LEN


def test_truncate_repr_returns_full_repr_when_short():
    class Sample:
        def __repr__(self):
            return "short"

    assert truncate_repr(Sample()) == "short"


def test_truncate_repr_returns_full_repr_when_under_custom_max():
    class Sample:
        def __repr__(self):
            return "ok"

    assert truncate_repr(Sample(), max_len=10) == "ok"


def test_truncate_repr_skips_truncation_when_disabled(monkeypatch):
    class Sample:
        def __repr__(self):
            return "Z" * (config.TRUNCATE_REPR_MAX_LEN + 50)

    monkeypatch.setattr(common, "TRUNCATE_REPR", False)
    assert truncate_repr(Sample()) == "Z" * (config.TRUNCATE_REPR_MAX_LEN + 50)
