from itertools import accumulate, repeat, takewhile


def iterate(func, x):
    """Iterate a function until it returns None."""
    yield from accumulate(repeat(func), lambda a, f: f(a), initial=x)


def iteratewhile(cond, func, x):
    yield from takewhile(cond, iterate(func, x))
