# https://adventofcode.com/2024/day/21

from functools import cache

from aoctk.data import M4
from aoctk.data import bij as _bij
from aoctk.input import get_lines


class bij(_bij):
    def __hash__(self):
        return id(self)


NUMPAD = bij(
    {
        "A": 2 + 3j,
        "0": 1 + 3j,
        "1": 2j,
        "2": 1 + 2j,
        "3": 2 + 2j,
        "4": +1j,
        "5": 1 + 1j,
        "6": 2 + 1j,
        "7": 0,
        "8": 1,
        "9": 2,
    }
)

DPAD = bij(
    {
        "A": 2,
        "^": 1,
        "v": 1 + 1j,
        "<": 1j,
        ">": 2 + 1j,
    }
)


@cache
def paths(pad: bij, a: str, b: str) -> list[str]:
    z, w = pad[a], pad[b]
    ps, q = [], [[z]]
    while q:
        if (p := q.pop(0))[-1] == w:
            ps.append(p)
        else:
            c = p[-1]
            dx = w.real - c.real
            dy = w.imag - c.imag
            if dx and (d := c + dx / abs(dx)) in pad.range:
                q.append([*p, d])
            if dy and (d := c + 1j * dy / abs(dy)) in pad.range:
                q.append([*p, d])

    return ["".join(M4.inv.get(y - x, "A") for x, y in zip(p, p[1:])) for p in ps]


@cache
def cost(pad: bij, a: str, b: str, n: int) -> int:
    return (
        min(
            sum(cost(DPAD, x, y, n - 1) for x, y in zip("A" + p, p + "A"))
            for p in paths(pad, a, b)
        )
        if n > 0
        else 1
    )


def solve(data: str, n: int) -> int:
    return sum(
        int(ln[:-1]) * sum(cost(NUMPAD, a, b, n + 1) for a, b in zip("A" + ln, ln))
        for ln in get_lines(data)
    )


def part_one(data="input.txt"):
    return solve(data, 2)


def part_two(data="input.txt"):
    return solve(data, 25)


def test():
    assert (_ := part_one("test.txt")) == 126384, _
