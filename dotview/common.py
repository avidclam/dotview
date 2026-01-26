from .config import TRUNCATE_REPR, TRUNCATE_REPR_MIN_LEN, TRUNCATE_REPR_MAX_LEN


def truncate(string, padding :str='...', max_len :int|None=None):
    """Return a truncated string."""
    padding_length = len(padding)
    if max_len is None:
        max_len = padding_length
    if max_len < padding_length:
        max_len = padding_length
    if len(string) > max_len:
        return f'{string[:max_len - padding_length]}{padding}'
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
