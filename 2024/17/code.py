# https://adventofcode.com/2024/day/17

from aoctk.input import get_groups


class StrangeDevice:
    __opmap__ = {}

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

        self.ip = 0

        self.stdout = []

        for f in dir(self):
            if hasattr(getattr(self, f), "__opcode__"):
                self.__opmap__[getattr(getattr(self, f), "__opcode__")] = getattr(
                    self, f
                )

    def combo(self, n):
        match n:
            case n if n <= 3:
                return n
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case 7:
                raise RuntimeError("Invalid combo operand")

    def opcode(n):
        def _(f):
            f.__opcode__ = n
            return f

        return _

    @opcode(0)
    def adv(self, oparg):
        self.a >>= self.combo(oparg)

    @opcode(1)
    def bxl(self, oparg):
        self.b ^= oparg

    @opcode(2)
    def bst(self, oparg):
        self.b = self.combo(oparg) & 7

    @opcode(3)
    def jnz(self, oparg):
        if self.a != 0:
            self.ip = oparg - 2

    @opcode(4)
    def bxc(self, oparg):
        self.b ^= self.c

    @opcode(5)
    def out(self, oparg):
        self.stdout.append(str(self.combo(oparg) & 7))

    @opcode(6)
    def bdv(self, oparg):
        self.b = self.a >> self.combo(oparg)

    @opcode(7)
    def cdv(self, oparg):
        self.c = self.a >> self.combo(oparg)

    def run(self, instrs):
        while self.ip < len(instrs):
            opcode, oparg = instrs[self.ip], instrs[self.ip + 1]
            self.__opmap__[opcode](oparg)
            self.ip += 2
        return ",".join(self.stdout)

    def __repr__(self):
        return f"StrangeDevice(a={self.a}, b={self.b}, c={self.c}, ip={self.ip})"


def part_one(data="input.txt"):
    rs, (p,) = get_groups(data)
    return StrangeDevice(*(int(_.partition(": ")[-1]) for _ in rs)).run(
        [int(_) for _ in p.partition(": ")[-1].split(",")]
    )


def part_two(data="input.txt"):
    def reverse(instrs):
        q, rinstrs = [(0, 0)], list(reversed(instrs))
        while q:
            a, i = q.pop(0)
            t, b = a, rinstrs[i]
            for a3 in range(8):
                t = a | a3
                if b == ((a3 ^ (t >> (a3 ^ 5))) ^ 3) & 7:
                    if i == len(instrs) - 1:
                        return t
                    q.append((t << 3, i + 1))
        raise RuntimeError("No solution found")

    _, (ps,) = get_groups(data)
    t = ps.partition(": ")[-1]
    assert t == StrangeDevice(
        a := reverse(p := [int(_) for _ in t.split(",")]), 0, 0
    ).run(p)
    return a


def test():
    assert (_ := part_one("test.txt")) == "4,6,3,5,6,3,5,2,1,0", _
