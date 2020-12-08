# https://adventofcode.com/2020/day/6

from functools import reduce
from typing import Callable, Generator


def groups(source: str, op: Callable[[set, set], set]) -> Generator[set, None, None]:
    answers = []
    for _ in open(source):
        if _ == "\n":
            yield reduce(op, answers)
            answers = []
        else:
            answers.append(set(_[:-1]))
    if answers:
        yield reduce(op, answers)


assert 11 == sum(len(_) for _ in groups("test.txt", set.__or__))

print(sum(len(_) for _ in groups("input.txt", set.__or__)))


assert 6 == sum(len(_) for _ in groups("test.txt", set.__and__))

print(sum(len(_) for _ in groups("input.txt", set.__and__)))