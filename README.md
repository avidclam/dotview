# `dotview`

Lightweight attribute access for nested dictionaries, with explicit support for
missing values and safe traversal.

## Why

Working with nested config or JSON data often leads to repetitive indexing and
missing-key checks. Dotview provides:

- Attribute-style access via `DotView`
- A path-aware `TreeView` for navigation and mutation
- A singleton `NA` value that represents missing or non-computable results

## Installation

```bash
pip install dotview
```

Optional JSONPath support:

```bash
pip install dotview[jsonpath]
```

## Quick start

```python
from dotview import DotView, NA

data = {"a": {"b": 2}, "z": {"o": {"oo": 100}}}
dv = DotView(data)

assert dv.a.b == 2
dv.z.o.ooo = -10
assert data["z"]["o"]["ooo"] == -10

# Missing paths return NA
assert dv.a.missing is NA
```

## DotView behavior

`DotView` wraps a `TreeView` and returns nested `DotView` objects for mapping
values. For scalars, it returns the scalar value directly.

```python
from dotview import DotView, NA

dv = DotView({"a": {"b": 2}})

assert dv.a.b == 2

# Attribute chains stop at scalars
try:
    _ = dv.a.b.c
except AttributeError:
    pass

# But the path lookup works and returns NA
assert dv["a", "b", "c"] is NA
```

### Special tuple keys

`DotView.__getitem__` supports special keys using `(..., "key")`:

- `(..., "data")` - underlying data mapping
- `(..., "root")` - current root path (tuple)
- `(..., "value")` - current value at root
- `(..., "parent")` - parent `TreeView`

```python
from dotview import DotView

dv = DotView({"a": {"b": 2}})
assert dv[..., "root"] == ()
assert dv[..., "value"] == {"a": {"b": 2}}
```

## TreeView

`TreeView` tracks a root path into a shared underlying mapping. It can be used
directly when you want explicit navigation and mutation without attribute access.

Key ideas:

- `TreeView.value` returns the value at the current path or `NA` if missing
- Assigning through a `TreeView` updates the underlying mapping
- Non-mapping input is wrapped as `{"data": <value>}`

## NA

`NA` is a singleton sentinel for missing values. It is falsy and propagates
through arithmetic and comparisons instead of raising.

```python
from dotview import NA

assert bool(NA) is False
assert (NA == 1) is NA
assert (NA + 1) is NA
```

## JSONPath (optional)

JSONPath helpers live in `dotview.jsonpath` and require `jsonpath_ng`.

```python
from dotview.jsonpath import get_path_values

data = {"a": {"b": 2}, "items": [{"x": 1}, {"x": 2}]}
assert get_path_values(data, "$.a.b") == [2]
assert get_path_values(data, "$.items[*].x") == [1, 2]
```

The helper accepts `TreeView` and `DotView` instances, returns `[]` for
non-collection inputs, and raises `ImportError` if the optional dependency is
missing.

## Configuration

String representations of `TreeView` data are truncated for readability.
The behavior can be configured in `dotview/config.py`:

- `TRUNCATE_REPR`
- `TRUNCATE_REPR_MIN_LEN`
- `TRUNCATE_REPR_MAX_LEN`
```
