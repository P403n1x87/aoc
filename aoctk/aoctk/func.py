from itertools import accumulate, islice, repeat, takewhile, tee


def iterate(func, x):
    """Iterate a function until it returns None."""
    yield from accumulate(repeat(func), lambda a, f: f(a), initial=x)


def iteratewhile(cond, func, x):
    yield from takewhile(cond, iterate(func, x))


def window(iterable, size):
    yield from zip(*(islice(t, i, None) for i, t in enumerate(tee(iterable, size))))
