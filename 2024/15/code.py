# https://adventofcode.com/2024/day/15

from aoctk.data import M4
from aoctk.data import Bounded2DGrid as G
from aoctk.input import get_groups


def part_one(data="input.txt"):
    g, ms = get_groups(data)
    wh = G.from_group(g)
    (r,) = (_ for _, v in wh.items() if v == "@")

    for m in "".join(ms):
        p, d = r, M4[m]
        while wh.get(p + d) != "#":
            if (p := p + d) not in wh:
                break
        else:
            continue

        while p != r:
            wh[p] = wh[p - d]
            p -= d

        del wh[r]

        r += d

    return int(sum(b.real + 100 * b.imag for b, v in wh.items() if v == "O"))


def part_two(data="input.txt"):
    def cluster(d: complex, ps: set) -> set | None:
        if not ps:
            return ps

        # Complete boxes
        ps |= {_ + {"[": 1, "]": -1}[wh[_]] for _ in ps}

        # Check if any boxes are touching a wall
        if any(wh.get(p + d) == "#" for p in ps):
            return None

        try:
            return ps | cluster(d, {p + d for p in ps if p + d in wh})
        except TypeError:
            return None

    g, ms = get_groups(data)
    wh = G.from_group(
        (
            _.replace("#", "##")
            .replace("O", "[]")
            .replace(".", "..")
            .replace("@", "@.")
            for _ in g
        )
    )
    (r,) = (_ for _, v in wh.items() if v == "@")

    for m in "".join(ms):
        p, d = r, M4[m]

        if d.imag and p + d in wh and wh[p + d] != "#":
            if (c := cluster(d, {r + d})) is None:
                continue

            # Move the cluster of boxes
            bs = {p: wh[p] for p in c}
            for p in c:
                del wh[p]
            for p, b in bs.items():
                wh[p + d] = b

            # Move the robot
            wh[r + d] = wh[r]
        else:
            while wh.get(p + d) != "#":
                if (p := p + d) not in wh:
                    break
            else:
                continue

            while p != r:
                wh[p] = wh[p - d]
                p -= d

        del wh[r]
        r += d

    return int(sum(b.real + 100 * b.imag for b, v in wh.items() if v == "["))


def test():
    assert (_ := part_one("test.txt")) == 10092, _
    assert (_ := part_two("test.txt")) == 9021, _
