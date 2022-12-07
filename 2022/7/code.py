# https://adventofcode.com/2022/day/7

import typing as t
from dataclasses import dataclass
from pathlib import Path

from aoctk.input import get_lines


@dataclass
class Dir:
    path: Path
    files: t.List[int]
    dirs: t.List["Dir"]
    parent: t.Optional["Dir"] = None

    def size(self) -> int:
        return sum(self.files) + sum(d.size() for d in self.dirs)

    def __hash__(self):
        return hash(self.path)


def get_fs(data: str) -> dict[Path, Dir]:
    lines = get_lines(data)
    line = next(lines)
    cwd = None
    fs: dict[Path, Dir] = {}

    def cd(_, path):
        nonlocal cwd

        if path == "/":
            cwd = Dir(Path("/"), [], [], None)
        elif path == "..":
            cwd = cwd.parent
        else:
            new_cwd = Dir(cwd.path / path, [], [], cwd)
            cwd.dirs.append(new_cwd)
            cwd = new_cwd

    def ls(output):
        for o in output:
            if not o.startswith("dir"):
                s, _ = o.split()
                cwd.files.append(int(s))
        fs[cwd.path] = cwd

    while line:
        cmd, *args = line[2:].split()
        output = []
        line = next(lines)

        while not line.startswith("$"):
            output.append(line)
            try:
                line = next(lines)
            except StopIteration:
                line = None
                break

        {"cd": cd, "ls": ls}[cmd](output, *args)

    return fs


def part_one(data="input.txt"):
    return sum(_ for _ in (d.size() for d in get_fs(data).values()) if _ < 100000)


def part_two(data="input.txt"):
    fs = get_fs(data)
    needed = -40000000 + fs[Path("/")].size()

    return min(_ for _ in (d.size() for d in fs.values()) if _ > needed)


def test():
    assert part_one("test.txt") == 95437
    assert part_two("test.txt") == 24933642
