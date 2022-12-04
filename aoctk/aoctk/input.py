import sys
import typing as t
from itertools import islice
from pathlib import Path
from types import FrameType


def get_path(filename: str = "input.txt") -> Path:
    """Get the path to the input file.

    The file is expected to reside within the directory of the calling script.
    """
    frame = t.cast(FrameType, sys._getframe(1))
    parent = Path(__file__).parent

    while parent in Path(frame.f_code.co_filename).parents:
        frame = t.cast(FrameType, frame.f_back)

    return Path(frame.f_code.co_filename).parent / filename


def get_lines(filename: str = "input.txt") -> t.Generator[str, None, None]:
    """Get the lines from the input file."""
    return (_.strip() for _ in get_path(filename).open())


def get_groups(
    filename: str = "input.txt",
    transformer: t.Callable[[str], t.Any] = lambda _: _,
) -> t.Generator[t.Tuple[t.Any, ...], None, None]:
    """Get groups of lines from the input file.

    Groups are separated by blank lines. Each line can be transformed prior to
    grouping by passing a transformer function.
    """
    group = []

    for line in get_lines(filename):
        if line:
            group.append(transformer(line))
        else:
            yield tuple(group)
            group.clear()

    if group:
        yield tuple(group)


def get_many(
    filename: str = "input.txt",
    n: int = 1,
    transformer: t.Callable[[str], t.Any] = lambda _: _,
) -> t.Generator[t.Tuple[t.Any, ...], None, None]:
    """Get groups of n lines from the input file.

    Elements can be transformed during grouping by providing a transformer
    function.
    """
    lines = get_lines(filename)
    yield from iter(lambda: tuple(transformer(_) for _ in islice(lines, n)), ())


def get_tuples(
    filename: str = "input.txt",
    sep: str = " ",
    transformer: t.Callable[[str], t.Any] = lambda _: _,
) -> t.Generator[t.Tuple[t.Any, ...], None, None]:
    """Get groups of lines from the input file.

    Groups are separated by blank lines. Each line can be transformed prior to
    grouping by passing a transformer function.
    """
    return (tuple(transformer(_) for _ in r.split(sep)) for r in get_lines(filename))
