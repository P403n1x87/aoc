# https://adventofcode.com/2020/day/14

from abc import ABC, abstractmethod
from typing import Any, Generator

MASK36 = (1 << 36) - 1


class Dock(ABC):
    def __init__(self) -> None:
        self.mask: Any = None
        self.mem: dict[int, int] = {}

    def eval(self, ins: str) -> None:
        op, _, val = ins.partition(" = ")
        if op == "mask":
            self.on_mask(val)
        else:
            self.on_mem(int(op[4:-1]), int(val))

    @abstractmethod
    def on_mask(self, val: int) -> None:
        ...

    @abstractmethod
    def on_mem(self, addr: int, val: int) -> None:
        ...

    def run(self, source: str) -> int:
        for _ in open(source):
            self.eval(_[:-1])
        return sum(self.mem.values())


class DockV1(Dock):
    def on_mask(self, val: int) -> None:
        orm, andm = 0, MASK36
        for c in val:
            if c == "0":
                andm &= MASK36 - 1
            elif c == "1":
                orm |= 1
            orm <<= 1
            andm = (andm << 1) & MASK36 | 1

        self.mask = (orm >> 1, andm >> 1 | (1 << 35))

    def on_mem(self, addr: int, val: int) -> None:
        orm, andm = self.mask
        self.mem[addr] = val & andm | orm


class DockV2(Dock):
    def on_mask(self, val: int) -> None:
        orm, flm = 0, 0
        for c in val:
            if c == "1":
                orm |= 1
            elif c == "X":
                flm |= 1
            orm <<= 1
            flm <<= 1
        self.mask = (orm >> 1, flm >> 1)

    def on_mem(self, addr: int, val: int) -> None:
        def floats(v: int, n: int) -> Generator[int, None, None]:
            if n < 0:
                yield 0
                return
            if v & (b := 1 << n):
                yield from (b | f for f in floats(v, n - 1))
            yield from floats(v, n - 1)

        orm, flm = self.mask
        base = (addr | orm) & (MASK36 - flm)
        for f in floats(flm, 35):
            self.mem[base | f] = val


assert 165 == DockV1().run("test.txt")
print(DockV1().run("input.txt"))

assert 208 == DockV2().run("test2.txt")
print(DockV2().run("input.txt"))