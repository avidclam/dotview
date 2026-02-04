from .config import TRUNCATE_REPR, TRUNCATE_REPR_MIN_LEN, TRUNCATE_REPR_MAX_LEN


def truncate(string, padding :str='...', max_len :int|None=None):
    """Return a truncated string."""
    if max_len is not None and len(string) > max_len:
        return f'{string[:max(max_len - len(padding), 0)]}{padding}'[:max_len]
    return string

def truncate_repr(obj, padding: str='...', max_len :int|None=None):
    """Return a truncated string representation of an object."""
    if not TRUNCATE_REPR:
        return repr(obj)
    if max_len is None:
        max_len = TRUNCATE_REPR_MAX_LEN
    if max_len < TRUNCATE_REPR_MIN_LEN:
        max_len = TRUNCATE_REPR_MIN_LEN
    return truncate(repr(obj), padding, max_len)
