# https://adventofcode.com/2022/day/10

from itertools import count

from aoctk.input import get_lines


def part_one(data="input.txt"):
    t = x = 1
    c = count(start=20, step=40)
    cc = next(c)
    ss = []
    for ins in get_lines(data):
        if ins == "noop":
            t += 1
            if t >= cc:
                ss.append(x * cc)
                cc = next(c)
        else:
            _, _, n = ins.partition(" ")
            t += 2
            if t > cc:
                ss.append(x * cc)
                cc = next(c)
            x += int(n)
            if t == cc:
                ss.append(x * cc)
                cc = next(c)
    return sum(ss)


def part_two(data="input.txt"):
    class CRT:
        def __init__(self):
            self.p = 0
            self.b = ""

        def draw(self, s):
            if self.p == 0:
                self.b += "\n"
            self.b += "#" if s - 1 <= self.p <= s + 1 else "."
            self.p = (self.p + 1) % 40

        def __str__(self):
            return self.b

    s, d = 1, CRT()
    for ins in get_lines(data):
        d.draw(s)
        if ins != "noop":
            d.draw(s)
            s += int(ins.partition(" ")[-1])

    return str(d)


def test():
    assert part_one("test.txt") == 13140
    assert (
        part_two("test.txt")
        == """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....\
"""
    )
