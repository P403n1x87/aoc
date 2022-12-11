from functools import reduce
from operator import mul


def prod(iterable, start=1):
    """Return the product of all elements in the iterable."""
    return reduce(mul, iterable, start)
