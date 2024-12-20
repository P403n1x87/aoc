from functools import cache


@cache
def _manhattan2d(d: complex) -> int:
    return int(abs(d.real) + abs(d.imag))


def manhattan2d(z: complex, w: complex = 0) -> int:
    return _manhattan2d(z - w)
