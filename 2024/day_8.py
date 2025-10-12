from __future__ import annotations

import itertools
import re
from collections import defaultdict
from itertools import permutations
from typing import Literal

from util.models import Coordinate, Size


def solve(part: Literal["a", "b"], input: str) -> int:
    antennas: dict[str, list[Coordinate]] = defaultdict(list)
    lines = input.splitlines()
    for row, line in enumerate(lines):
        for match in re.finditer(r"[a-zA-Z0-9]", line):
            antennas[match.group()].append(Coordinate(row, match.start()))

    antinodes: set[Coordinate] = set()
    size = Size(len(lines), len(lines[0]))

    for _, antenna_list in antennas.items():
        for a, b in permutations(antenna_list, 2):
            if part == "a":
                antinode = a + (a - b)  # reflects b across a
                if antinode.in_range(size):
                    antinodes.add(antinode)
            else:
                step = (b - a).normalize()
                antinodes |= set(
                    itertools.takewhile(
                        lambda n: n.in_range(size), (b + step * i for i in itertools.count(0))
                    )
                )
                antinodes |= set(
                    itertools.takewhile(
                        lambda n: n.in_range(size), (a - step * i for i in itertools.count(0))
                    )
                )

    return len(antinodes)
