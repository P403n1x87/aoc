# https://adventofcode.com/2020/day/8

from dataclasses import dataclass
from typing import Tuple


class InfiniteLoop(Exception):
    pass


@dataclass
class Instruction:
    code: str
    op: int

    @staticmethod
    def parse(ins: str) -> "Instruction":
        code, _, op = ins.partition(" ")
        return Instruction(code, int(op))


class Machine:
    def __init__(self) -> None:
        self.reset()
        self.tape = []

    def reset(self) -> None:
        self.ip = 0
        self.acc = 0
        self.visited = set()

    def load(self, source: str) -> None:
        self.reset()
        self.tape = [Instruction.parse(_[:-1]) for _ in open(source)]

    @property
    def state(self) -> Tuple[int]:
        return (self.ip,)

    def run(self) -> None:
        while self.ip < len(self.tape):
            state = self.state
            if state in self.visited:
                raise InfiniteLoop()
            self.visited.add(state)

            ins = self.tape[self.ip]
            getattr(self, "on_" + ins.code)(ins.op)
            self.ip += 1

    def on_nop(self, op: int = None) -> None:
        pass

    def on_acc(self, op: int = None) -> None:
        self.acc += op

    def on_jmp(self, op: int = None) -> None:
        self.ip += op - 1

    def patch(self) -> None:
        self.reset()
        try:
            self.run()
        except InfiniteLoop:
            r = {"jmp": "nop", "nop": "jmp"}
            for (i,) in self.visited:
                ins = self.tape[i]
                if ins.code in r:
                    old_ins = ins
                    self.tape[i] = Instruction(r[ins.code], ins.op)
                    self.reset()
                    try:
                        self.run()
                    except InfiniteLoop:
                        self.tape[i] = old_ins
                        continue
                    return


try:
    m = Machine()
    m.load("test.txt")
    m.run()
except InfiniteLoop:
    assert m.acc == 5


try:
    m = Machine()
    m.load("input.txt")
    m.run()
except InfiniteLoop:
    print(m.acc)
    m.patch()
    print(m.acc)