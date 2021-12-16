# https://adventofcode.com/2021/day/16

import os
from dataclasses import dataclass
from typing import List


def resolve(name="input.txt"):
    return os.path.join(os.path.dirname(__file__), name)


@dataclass
class Packet:
    version: int

    def vs(self):
        return self.version


@dataclass
class LiteralPacket(Packet):
    literal: int

    def eval(self):
        return self.literal


@dataclass
class OperatorPacket(Packet):
    opcode: int
    operands: List[Packet]

    def eval(self):
        if self.opcode == 0:
            return sum(_.eval() for _ in self.operands)
        if self.opcode == 1:
            return eval("*".join(str(_.eval()) for _ in self.operands))
        if self.opcode == 2:
            return min(_.eval() for _ in self.operands)
        if self.opcode == 3:
            return max(_.eval() for _ in self.operands)
        if self.opcode == 5:
            a, b = self.operands
            return a.eval() > b.eval()
        if self.opcode == 6:
            a, b = self.operands
            return a.eval() < b.eval()
        if self.opcode == 7:
            a, b = self.operands
            return a.eval() == b.eval()

    def vs(self):
        return super().vs() + sum(_.vs() for _ in self.operands)


@dataclass
class Scanner:
    buffer: str
    pos: int = 0

    def __getitem__(self, item):
        if isinstance(item, slice):
            try:
                return self.buffer[
                    slice((item.start or 0) + self.pos, item.stop + self.pos)
                ]
            except IndexError:
                return ""
        return self.buffer[item + self.pos]

    def __bool__(self):
        return len(self.buffer) - self.pos >= 11

    def get(self, size):
        try:
            return self[:size]
        finally:
            self.pos += size

    def getint(self, size):
        return int(self.get(size), 2)


def parse(scanner, maxpackets=None):
    c = 0
    while scanner:
        v, t = scanner.getint(3), scanner.getint(3)
        if t == 4:
            literal = ""
            while True:
                h, *tail = scanner.get(5)
                literal += "".join(tail)
                if h == "0":
                    break
            yield LiteralPacket(version=v, literal=int(literal, 2))
        else:
            yield OperatorPacket(
                version=v,
                opcode=t,
                operands=list(parse(Scanner(scanner.get(scanner.getint(15)))))
                if scanner.get(1) == "0"
                else list(parse(scanner, scanner.getint(11))),
            )

        c += 1
        if maxpackets is not None and c >= maxpackets:
            break


def solve(datafile="input.txt"):
    with open(resolve(datafile)) as f:
        parsed = list(
            parse(
                Scanner(
                    "".join(
                        [bin(int(_, 16))[2:].zfill(4) for _ in f.readline().strip()]
                    )
                )
            )
        )
        return sum(_.vs() for _ in parsed), sum(_.eval() for _ in parsed)


def test():
    assert [LiteralPacket(version=6, literal=2021)] == list(
        parse(Scanner("".join([bin(int(_, 16))[2:].zfill(4) for _ in "D2FE28"])))
    )

    assert [
        OperatorPacket(
            version=1, opcode=6, operands=[LiteralPacket(6, 10), LiteralPacket(2, 20)]
        )
    ] == list(
        parse(
            Scanner("".join([bin(int(_, 16))[2:].zfill(4) for _ in "38006F45291200"]))
        )
    )

    assert [
        OperatorPacket(
            version=7,
            opcode=3,
            operands=[LiteralPacket(2, 1), LiteralPacket(4, 2), LiteralPacket(1, 3)],
        )
    ] == list(
        parse(
            Scanner("".join([bin(int(_, 16))[2:].zfill(4) for _ in "EE00D40C823060"]))
        )
    )

    assert solve("test.txt")[0] == 16
    assert solve("test2.txt")[0] == 12
    assert solve("test3.txt")[0] == 23

    assert solve("test4.txt")[1] == 3


test()
print(solve())
