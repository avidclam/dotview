class NAType:
    """Singleton type representing a missing or non-computable value.

    `NA` behaves similarly to `None` in boolean contexts (i.e., it is falsy),
    but differs in that it explicitly propagates through arithmetic and
    comparison operations instead of raising or returning concrete values.

    There is exactly one instance of this type: `NA`.
    """

    _instance = None

    def __new__(cls):
        """Create or return the singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self):
        """Return the canonical string representation."""
        return "<NA>"

    def __str__(self):
        """Return the human-readable string representation."""
        return "<NA>"

    # ------------------------------------------------------------------
    # Boolean behavior
    # ------------------------------------------------------------------

    def __bool__(self):
        """Return False, matching the behavior of None.

        This allows `NA` to be used safely in boolean contexts such as
        `if` statements and logical expressions without raising.
        """
        return False

    # ------------------------------------------------------------------
    # Comparison behavior (unknown result)
    # ------------------------------------------------------------------

    def __eq__(self, other):
        """Return NA for equality comparisons."""
        return self

    def __ne__(self, other):
        """Return NA for inequality comparisons."""
        return self

    def __lt__(self, other):
        """Return NA for less-than comparisons."""
        return self

    def __le__(self, other):
        """Return NA for less-than-or-equal comparisons."""
        return self

    def __gt__(self, other):
        """Return NA for greater-than comparisons."""
        return self

    def __ge__(self, other):
        """Return NA for greater-than-or-equal comparisons."""
        return self

    # ------------------------------------------------------------------
    # Arithmetic propagation
    # ------------------------------------------------------------------

    def _propagate(self, *args, **kwargs):
        """Propagate NA through arithmetic operations."""
        return self

    __add__ = __radd__ = _propagate
    __sub__ = __rsub__ = _propagate
    __mul__ = __rmul__ = _propagate
    __truediv__ = __rtruediv__ = _propagate
    __floordiv__ = __rfloordiv__ = _propagate
    __mod__ = __rmod__ = _propagate
    __pow__ = __rpow__ = _propagate

    # Unary operators
    __neg__ = __pos__ = __abs__ = _propagate

    # ------------------------------------------------------------------
    # Copy semantics
    # ------------------------------------------------------------------

    def __copy__(self):
        """Return the singleton instance."""
        return self

    def __deepcopy__(self, memo):
        """Return the singleton instance."""
        return self


# Public singleton instance
NA = NAType()
