from collections.abc import Mapping
from .treeview import TreeView


class DotView:
    """Attribute-based access to nested dictionary data (e.g., config.main.storage.path).

    The underlying data is not isolated from the initial input.
    Modifications through DotView affect the original input dictionary.

    Args:
        data: in any form including TreeView or Mapping.
    """
    _protected_from_setattr = ('_tree_view',)

    def __init__(self, data):
        if isinstance(data, DotView):
            self._tree_view = data._tree_view
        elif isinstance(data, TreeView):
            self._tree_view = data
        else:
            self._tree_view = TreeView(data, ())

    def __getitem__(self, key):
        if isinstance(key, tuple) and len(key) > 1 and key[0] == Ellipsis:
            special_key = key[1]
            # Special cases are:
            # (..., 'data') - get underlying data
            # (..., 'root') - get current root path
            # (..., 'value') - get current root value
            # (..., 'parent') - get parent view
            return getattr(self._tree_view, special_key)
        key_tree_view = self._tree_view[key]
        key_tree_view_value = key_tree_view.value
        if isinstance(key_tree_view_value, Mapping):
            return self.__class__(key_tree_view)
        return key_tree_view_value

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        if key in self._protected_from_setattr:
            super().__setattr__(key, value)
        else:
            self._tree_view[key] = value

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self._tree_view)})'
