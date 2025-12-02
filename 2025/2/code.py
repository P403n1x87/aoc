# https://adventofcode.com/2025/day/2

from aoctk.input import get_tuples


def part_one(data="input.txt"):
    (line,) = get_tuples(data, sep=",")
    ns = set()
    for r in line:
        a, b = r.split("-")
        na, nb = int(a), int(b)
        la, lb = len(a), len(b)
        l = (la >> 1) + (la & 1)
        h = max(l, lb >> 1)
        for s in range(l, h + 1):
            c = 10 ** (s - 1)
            while (m := int(f"{c}{c}")) <= nb:
                if m >= na:
                    ns.add(m)
                c += 1
    return sum(ns)


def part_two(data="input.txt"):
    (line,) = get_tuples(data, sep=",")
    ns = set()
    for r in line:
        a, b = r.split("-")
        na, nb = int(a), int(b)
        la, lb = len(a), len(b)
        for s in range(1, (lb >> 1) + 1):
            if lb % s != 0 and la % s != 0:
                continue
            for v in (la, lb):
                if (q := v // s) <= 1:
                    continue
                c = 10 ** (s - 1)
                while (m := int(str(c) * q)) <= nb:
                    if m >= na:
                        ns.add(m)
                    c += 1
    return sum(ns)


def test():
    assert (_ := part_one("test.txt")) == 1227775554, _
    assert (_ := part_two("test.txt")) == 4174379265, _
