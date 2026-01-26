from collections.abc import Sequence, Mapping
from .treeview import TreeView
from .dotview import DotView
try:
    import jsonpath_ng
except ImportError:
    jsonpath_ng = None


def get_path_values(data, path: str):
    "Retrieves the list of values given JSON Path"
    if jsonpath_ng is None:
        raise ImportError("jsonpath_ng is not installed, please make sure dotview is installed as dotview[jsonpath]")
    if isinstance(data, TreeView):
        data = data.value
    elif isinstance(data, DotView):
        data = data[..., 'value']
    if not isinstance(data, Mapping) and not isinstance(data, Sequence):
        return []
    return [match.value for match in jsonpath_ng.parse(path).find(data)]
