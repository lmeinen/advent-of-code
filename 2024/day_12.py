from __future__ import annotations

from typing import Literal

from util.algs import bfs
from util.models import Size, Vec


def solve(part: Literal["a", "b"], input: str) -> int:
    grid = [list(row) for row in input.splitlines()]
    size = Size(len(grid), len(grid[0]))
    unmarked = set(size.range())

    def neighbours(plot: Vec) -> list[Vec]:
        orthogonal = [
            plot + (step * sign) for sign in [-1, 1] for step in [Vec(0, 1), Vec(1, 0)]
        ]
        return [n for n in orthogonal if n.in_range(size) and type(plot) == type(n)]

    def perimeter(plot: Vec) -> int:
        return 4 - len(neighbours(plot))

    def type(plot: Vec) -> str:
        return grid[plot.x][plot.y]

    def corners(plot: Vec) -> int:
        # eight types of corners to check (inside/outside * 4)
        ns = neighbours(plot)

        orthogonal = [
            plot + (step * sign) for sign in [-1, 1] for step in [Vec(1, 0), Vec(0, 1)]
        ]

        diagonals = [
            plot - Vec(1, 1),
            plot + Vec(1, -1),
            plot + Vec(1, 1),
            plot - Vec(1, -1),
        ]

        cs = [
            1
            for a, b, c in zip(orthogonal, orthogonal[1:] + orthogonal[:1], diagonals)
            if (not (a in ns or b in ns))
            or (a in ns and b in ns and type(c) != type(plot))
        ]

        return len(cs)

    price = 0
    while unmarked:
        region = set(bfs(unmarked.pop(), neighbours))
        unmarked -= region
        price += len(region) * sum(
            ((perimeter(p) if part == "a" else corners(p)) for p in region)
        )
    return price
