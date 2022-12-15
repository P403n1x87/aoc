import typing as t


def manhattan2d(z: complex, w: t.Optional[complex] = None) -> int:
    d = z - w if w is not None else z
    return int(abs(d.real) + abs(d.imag))
