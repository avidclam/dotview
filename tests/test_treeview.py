from dotview import TreeView, NA


def test_treeview_init_with_non_mapping_wraps_data():
    tv = TreeView(123)
    assert tv.data == {"data": 123}
    assert tv.root == ("data",)
    assert tv.value == 123


def test_treeview_init_with_mapping_keeps_reference():
    data = {"a": {"b": 2}}
    tv = TreeView(data)
    assert tv.data is data
    assert tv.root == ()


def test_treeview_init_with_treeview_shares_data():
    data = {"a": 1}
    base = TreeView(data, ("a",))
    tv = TreeView(base)
    assert tv.data is data


def test_treeview_parent_and_value():
    data = {"a": {"b": 2}}
    tv = TreeView(data, ("a", "b"))
    assert tv.value == 2
    assert tv.parent.value == {"b": 2}


def test_treeview_value_missing_returns_na():
    tv = TreeView({"a": {}})
    assert tv["a", "missing"].value is NA


def test_treeview_setitem_creates_nested_mapping():
    data = {}
    tv = TreeView(data)
    tv["a", "b"] = 5
    assert data == {"a": {"b": 5}}


def test_treeview_setitem_replaces_non_mapping_parent():
    data = {"a": 1}
    tv = TreeView(data)
    tv["a", "b"] = 5
    assert data == {"a": {"b": 5}}


def test_treeview_getitem_accepts_scalar_or_sequence():
    data = {"a": {"b": 2}}
    tv = TreeView(data)
    assert tv["a"].root == ("a",)
    assert tv[("a", "b")].root == ("a", "b")


def test_treeview_value_setter_on_root_replaces_data():
    tv = TreeView({"a": 1})
    tv.value = {"b": 2}
    assert tv.data == {"b": 2}
