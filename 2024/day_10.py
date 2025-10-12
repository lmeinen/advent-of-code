from __future__ import annotations

from functools import cache
from typing import Literal

from util.algs import bfs
from util.models import Coordinate, Size


def solve(part: Literal["a", "b"], input: str) -> int:
    grid: list[list[int]] = []
    trailheads: list[Coordinate] = []

    for x, line in enumerate(input.splitlines()):
        heights = list(map(int, line))
        grid.append(heights)
        trailheads.extend(
            [Coordinate(x, y) for y, height in enumerate(heights) if height == 0]
        )

    size = Size(len(grid), len(grid[0]))

    def height(field: Coordinate) -> int:
        return grid[field.x][field.y]

    def neighbours(field: Coordinate) -> list[Coordinate]:
        return list(
            filter(
                lambda n: n.in_range(size) and height(n) == height(field) + 1,
                [
                    field + (step * sign)
                    for sign in [-1, 1]
                    for step in [Coordinate(0, 1), Coordinate(1, 0)]
                ],
            )
        )

    def peaks(field: Coordinate) -> int:
        """returns the number of peaks reachable from this field"""
        return len({f for f in bfs(field, neighbours) if height(f) == 9})

    @cache
    def trails(field: Coordinate) -> int:
        """returns the number of trails from this field"""
        if height(field) == 9:
            return 1
        return sum(
            [
                trails(neighbour)
                for neighbour in neighbours(field)
                if height(neighbour) == height(field) + 1
            ]
        )

    return sum([peaks(head) if part == "a" else trails(head) for head in trailheads])
