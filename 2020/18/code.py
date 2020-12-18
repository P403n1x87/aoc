from itertools import takewhile
from typing import Callable


iden = lambda x: x
literal = lambda n: lambda m: m(n)
addition = lambda n: lambda m: literal(n + m(iden))
multiplication = lambda n: lambda m: literal(n * m(iden))


def math(expr: str) -> tuple["literal", str]:
    op = iden
    while expr := expr.strip():
        if expr[0].isdigit():
            n = "".join(takewhile(str.isdigit, expr))
            n, expr = int(n), expr[len(n) :]
            op = op(literal(int(n)))
        elif expr[0] == "+":
            op = op(addition)
            expr = expr[2:]
        elif expr[0] == "*":
            op = op(multiplication)
            expr = expr[2:]
        elif expr[0] == "(":
            arg, expr = math(expr[1:])
            op = op(arg)
        elif expr[0] == ")":
            return op, expr[1:]
    return op, expr


def adv_math(expr: str, sub: bool = True) -> tuple["literal", str]:
    op = iden
    while expr := expr.strip():
        if expr[0].isdigit():
            n = "".join(takewhile(str.isdigit, expr))
            n, expr = int(n), expr[len(n) :]
            op = op(literal(int(n)))
        elif expr[0] == "+":
            op = op(addition)
            expr = expr[2:]
        elif expr[0] == "*":
            op = op(multiplication)
            rhs, expr = adv_math(expr[2:], False)
            op = op(rhs)
        elif expr[0] == "(":
            arg, expr = adv_math(expr[1:])
            op = op(arg)
        elif expr[0] == ")":
            return op, expr[sub and 1 or 0 :]
    return op, expr


def eval(expr: str, parser: Callable[[str], tuple["literal", str]]) -> int:
    res, expr = parser(expr)
    assert not expr
    return res(iden)


def solve(source: str) -> tuple[int, int]:
    return tuple(sum(eval(_, p) for _ in open(source)) for p in [math, adv_math])


assert 13632 == eval("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", math)
assert 23340 == eval("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", adv_math)
print(solve("input.txt"))
