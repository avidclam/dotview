from collections.abc import Sequence, Mapping
from .na import NA
from .common import truncate_repr


class TreeView:
    """View of nested dictionary data with a pointer to the current branch.

    TreeView provides navigation through dictionary data via a root pointer.
    It supports non-existent nodes through NA placeholders.

    The underlying data can be in any form; non-dict data is wrapped as {'data': data}.

    Args:
      data: in any form including TreeView or Mapping. Will be stored by reference.
      root: path to the current branch (tuple of keys)
    """

    def __init__(self, data: Mapping|None=None, root: Sequence|None=None):
        if data is None:
            data = {}
        if root is None:
            root = ()
        if isinstance(root, str) or not isinstance(root, Sequence):
            # Just in case ...
            self.root = (root,)
        else:
            self.root = tuple(root)
        if isinstance(data, TreeView):
            # Share data reference
            self.data = data.data
        elif isinstance(data, Mapping):
            # Store reference to incoming mapping
            self.data = data
        else:
            # Store arbitrary data in a dict mapping
            self.data = {'data': data}
            self.root = tuple(['data'] + list(self.root))

    def clone(self, new_root: Sequence|None=None):
        if new_root is None:
            new_root = self.root
        return self.__class__(self.data, new_root)

    @property
    def parent(self):
        if not self.root:
            return self
        return self.clone(self.root[:-1])


    @property
    def value(self):
        """Returns the object at the current branch.

        Returns either a Mapping/scalar at that path, or NA if a path doesn't exist.
        Modifications through a value object directly affect the underlying data.
        """
        data = self.data
        for k in self.root:
            if isinstance(data, Mapping) and k in data:
                data = data[k]
            else:
                return NA
        return data

    @value.setter
    def value(self, new_value):
        if self.root:
            key = self.root[-1]
            parent = self.parent
            value_object = parent.value
            if isinstance(value_object, Mapping):
                value_object[key] = new_value
            else:  # Non-dict or non-existent
                parent.value = {key: new_value}
        else:
            self.data = new_value

    def __getitem__(self, key):
        if isinstance(key, str) or not isinstance(key, Sequence):
            keys = [key]
        else:
            keys = list(key)
        return self.clone(list(self.root) + keys)

    def __setitem__(self, key, value):
        self.__getitem__(key).value = value

    def __repr__(self):
        # Truncate data for readable output
        data_str = truncate_repr(self.data)
        root_repr = repr(self.root)
        return f'{self.__class__.__name__}({data_str}, root={root_repr})'
