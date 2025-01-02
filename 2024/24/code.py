# https://adventofcode.com/2024/day/24

from collections import defaultdict

from aoctk.input import get_groups


def part_one(data="input.txt"):
    vs, gs = get_groups(data)
    ws = {}
    for v in vs:
        w, _, n = v.partition(": ")
        ws[w] = int(n)
    q = [
        g.replace("XOR", "^").replace("AND", "&").replace("OR", "|").split(" -> ")
        for g in gs
    ]
    while q:
        e, t = q.pop(0)
        try:
            ws[t] = eval(e, {}, ws)
        except NameError:
            q.append((e, t))

    return sum(1 << int(_[1:]) for _, v in ws.items() if v and _.startswith("z"))


class Gate:
    def __init__(self, type, inputs, output):
        self.type = type
        self.inputs = inputs
        self.output = output

    @classmethod
    def parse(cls, s):
        _, out = s.split(" -> ")
        i1, t, i2 = _.split(" ")
        return cls(t, {i1, i2}, out)

    def __repr__(self):
        return f" {self.type} ".join(sorted(self.inputs)) + f" -> {self.output}"


def part_two(data="input.txt"):
    _, gs = get_groups(data)

    xlate = {}

    def rename_output(g: Gate, n: str):
        o = g.output
        g.output = n
        for f in input_map[o]:
            f.inputs.remove(o)
            f.inputs.add(n)
        input_map[n] = input_map.pop(o)
        xlate[n] = o

    def swap_input(na, nb):
        ia = input_map[na]
        ib = input_map[nb]
        for g in ia:
            g.inputs.remove(na)
            g.inputs.add(nb)
        for g in ib:
            g.inputs.remove(nb)
            g.inputs.add(na)
        input_map[na] = ib
        input_map[nb] = ia

    def swap_output(na, nb):
        (ga,) = [g for g in gates if g.output == na]
        (gb,) = [g for g in gates if g.output == nb]
        ga.output = nb
        gb.output = na

    gates = [Gate.parse(g) for g in gs]
    input_map = defaultdict(list)
    for g in gates:
        for i in g.inputs:
            input_map[i].append(g)

    (c,) = (_ for _ in input_map["x00"] if _.type == "AND")
    rename_output(c, "c01")

    swaps = []
    for i in range(1, 45):
        xs = input_map[f"x{i:02d}"]
        for g in xs:
            if g.output.startswith("z"):
                # There must be a XOR with no x,y,z
                (t,) = (
                    f
                    for f in gates
                    if f.type == "XOR"
                    and all(
                        _[0] not in {"x", "y"} and f.output[0] != "z" for _ in f.inputs
                    )
                )
                swaps.extend((g.output, t.output))
                g.output, t.output = t.output, g.output
            rename_output(g, f"a{i:02d}" if g.type == "AND" else f"e{i:02d}")

        if all(_.type != "AND" for _ in input_map[f"e{i:02d}"]):
            swaps.extend((f"e{i:02d}", f"a{i:02d}"))
            swap_input(f"e{i:02d}", f"a{i:02d}")
        (dx,) = (_ for _ in input_map[f"e{i:02d}"] if _.type == "XOR")
        if dx.output != f"z{i:02d}":
            swaps.extend((f"z{i:02d}", dx.output))
            swap_output(f"z{i:02d}", dx.output)

        (c,) = input_map[f"a{i:02d}"]
        if c.output != "z45":
            rename_output(c, f"c{i+1:02d}")

    return ",".join(sorted(xlate.get(_, _) for _ in swaps))


def test():
    assert (_ := part_one("test.txt")) == 2024, _
