# https://adventofcode.com/2023/day/20

import typing as t
from collections import defaultdict, deque
from itertools import count
from math import lcm

from aoctk.input import get_lines


class Module:
    state: t.Any = None

    def operation(self, source_module: str, input: bool) -> t.Optional[bool]:
        return None

    def link(self, sources: list[str]) -> None:
        pass

    def __call__(self, source_module: str, input: bool):
        return self.operation(source_module, input)

    def freeze(self):
        return self.state


class FlipFlop(Module):
    def __init__(self):
        self.state = False

    def operation(self, source_module: str, input: bool) -> t.Optional[bool]:
        if input:
            return None
        self.state = not self.state
        return self.state


class Conjunction(Module):
    def link(self, sources: list[str]) -> None:
        self.state = {source: False for source in sources}

    def operation(self, source_module: str, input: bool) -> t.Optional[bool]:
        self.state[source_module] = input
        return not all(self.state.values())

    def freeze(self):
        return frozenset(self.state.items())


class Broadcaster(Module):
    def operation(self, source_module: str, input: bool) -> t.Optional[bool]:
        return input


ML = {"%": FlipFlop, "&": Conjunction, "b": Broadcaster}


def button(modules, targets, cb=None):
    ps, q = 0, deque([("button", False, {"roadcaster"})])
    while q:
        source, input, ts = q.popleft()
        ps += (1j**input) * len(ts)
        for tg in ts:
            output = modules[tg](source, input)
            if cb is not None:
                cb(source, input, tg, output)
            if output is not None:
                q.append((tg, output, targets[tg]))
    return ps


def parse(data: str) -> tuple[dict, dict]:
    ss, ts, ms = defaultdict(list), defaultdict(list), defaultdict(Module)

    for line in get_lines(data):
        s, _, tgs = line.partition(" -> ")
        ms[name := s[1:]] = ML[s[0]]()
        for tg in tgs.split(", "):
            ts[name].append(tg)
            ss[tg].append(name)
    for n, m in ms.items():
        m.link(ss[n])

    return ms, ts, ss


def part_one(data="input.txt"):
    ms, ts, _ = parse(data)
    states = {}
    for c in range(1000):
        if (state := frozenset((n, m.freeze()) for n, m in ms.items())) in states:
            break
        states[state] = button(ms, ts)
    i = list(states.keys()).index(state)
    p = c - i
    vs = list(states.values())
    q, r = divmod(1000 - i, p) if p else (0, 1000)
    return int((((sum(vs[: i + r])) + q * sum(vs[i : i + p])) ** 2).imag / 2)


def part_two(data="input.txt"):
    ms, ts, ss = parse(data)
    rxs, c, ps = ss["rx"][0], 0, {}
    n = len(ss[rxs])

    def cb(s, i, t, o):
        if i and t == rxs:
            ps.setdefault(s, c)

    for c in count(1):
        button(ms, ts, cb)
        if len(ps) == n:
            return lcm(*ps.values())


def test():
    assert part_one("test.txt") == 11687500
    # assert part_two("test.txt") == 1
