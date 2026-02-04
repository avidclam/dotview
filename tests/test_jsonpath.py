import pytest

from dotview import DotView, TreeView
from dotview import jsonpath as jsonpath_module


def test_jsonpath_requires_dependency(monkeypatch):
    monkeypatch.setattr(jsonpath_module, "jsonpath_ng", None)
    with pytest.raises(ImportError):
        jsonpath_module.get_path_values({"a": 1}, "$.a")


def test_jsonpath_gets_values_from_mapping():
    pytest.importorskip("jsonpath_ng")
    from dotview.jsonpath import get_path_values

    data = {"a": {"b": 2}, "items": [{"x": 1}, {"x": 2}]}
    assert get_path_values(data, "$.a.b") == [2]
    assert get_path_values(data, "$.items[*].x") == [1, 2]


def test_jsonpath_accepts_views():
    pytest.importorskip("jsonpath_ng")
    from dotview.jsonpath import get_path_values

    data = {"a": {"b": 2}}
    tv = TreeView(data)
    dv = DotView(data)

    assert get_path_values(tv, "$.a.b") == [2]
    assert get_path_values(dv, "$.a.b") == [2]


def test_jsonpath_non_collection_returns_empty_list():
    pytest.importorskip("jsonpath_ng")
    from dotview.jsonpath import get_path_values

    assert get_path_values(10, "$.a") == []
