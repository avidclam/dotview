import pytest

from dotview import DotView, TreeView, NA


def test_dotview_init_with_dotview_reuses_treeview():
    base = DotView({"a": {"b": 2}})
    dv = DotView(base)
    assert dv is not base
    assert dv[(..., "data")] is base[(..., "data")]
    assert dv[(..., "root")] is base[(..., "root")]
    assert dv[(..., "parent")] is base[(..., "parent")]
    assert dv[(..., "value")] is base[(..., "value")]


def test_dotview_init_with_treeview_reuses_view():
    tv = TreeView({"a": 1})
    dv = DotView(tv)
    assert dv[(..., "data")] is tv.data


def test_dotview_attribute_access_for_mapping():
    dv = DotView({"a": {"b": 2}})
    assert isinstance(dv.a, DotView)
    assert dv.a.b == 2


def test_dotview_item_access_for_scalar():
    dv = DotView({"a": 1})
    assert dv["a"] == 1


def test_dotview_setattr_sets_underlying_data():
    data = {"a": 1}
    dv = DotView(data)
    dv.b = 2
    assert data == {"a": 1, "b": 2}


def test_dotview_special_getitem_keys():
    data = {"a": {"b": 2}}
    dv = DotView(data)
    assert dv[(..., "data")] is data
    assert dv[(..., "root")] == ()
    assert dv[(..., "value")] == data
    assert isinstance(dv[(..., "parent")], TreeView)


def test_dotview_missing_path_returns_na():
    dv = DotView({"a": {}})
    assert dv.a.missing is NA


def test_dotview_attribute_chain_scalar_then_path_getitem_returns_na():
    dv = DotView({"a": {"b": 2}})
    assert dv.a.b == 2
    with pytest.raises(AttributeError):
        _ = dv.a.b.c
    assert dv["a", "b", "c"] is NA


def test_dotview_repr_includes_class_name():
    dv = DotView({"a": 1})
    assert "DotView(" in repr(dv)
