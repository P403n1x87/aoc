# https://adventofcode.com/2022/day/21

from aoctk.input import get_tuples


class Rules(dict):
    def __init__(self, data, override={}):
        super().__init__(get_tuples(data, ": "))
        self.update(override)

    def resolve(self, r="root"):
        if " " not in (desc := self[r]):
            return desc

        a, op, b = desc[:4], desc[5], desc[7:]

        return f"({self.resolve(a)} {op} {self.resolve(b)})"


def part_one(data="input.txt"):
    return int(eval(Rules(data).resolve()))


def part_two(data="input.txt"):
    rs = Rules(data, {"humn": "x"})
    root = rs["root"]

    f = lambda x: eval(rs.resolve(root[:4]), {"x": x})

    c = f(0)
    m = f(1) - c

    y = int(eval(rs.resolve(root[7:])))
    x = int((y - c) / m)

    # Very large rounding errors with big numbers
    while d := f(x) - y:
        x += -d / m

    return int(x)


def test():
    assert part_one("test.txt") == 152
    assert part_two("test.txt") == 301
