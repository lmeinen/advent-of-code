from __future__ import annotations

from typing import Literal

from util.models import Graph


def solve(part: Literal["a", "b"], input: str) -> int:

    dirs = ["E", "S", "W", "N"]

    def label(i: int, j: int, facing) -> str:
        return f"{i}/{j}/{facing}"

    grid = [list(row) for row in input.splitlines()]
    start = [
        label(i, j, "E")
        for i, row in enumerate(grid)
        for j in range(len(row))
        if grid[i][j] == "S"
    ][0]

    def is_corner(i, j: int) -> bool:
        ns = [grid[i - 1][j], grid[i][j + 1], grid[i + 1][j], grid[i][j - 1]]
        for k in range(2):
            if (
                ns[k] == "#"
                and ns[(k + 1) % 4] != "#"
                and ns[(k + 2) % 4] == "#"
                and ns[(k + 3) % 4] != "#"
            ):
                return False
        return True

    # (a) build graph
    start, end = None, None
    g = Graph()
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c != "#" and is_corner(i, j):
                ...

    for i, row in enumerate(input.splitlines()):
        for j, c in enumerate(row):
            if c != "#":
                for d in dirs:
                    g.add_node(label(i, j, d))
                for a, b in zip(dirs, [dirs[-1]] + dirs[:-1]):
                    g.add_edge((label(i, j, a), label(i, j, b)), weight=1000)
                for d in dirs:
                    g.add_node(label(i, j, d))
                if g.contains(label(i - 1, j, "N")):
                    g.add_edge((label(i - 1, j, "N"), label(i, j, "N")))
                if g.contains(label(i - 1, j, "S")):
                    g.add_edge((label(i - 1, j, "S"), label(i, j, "S")))
                if g.contains(label(i, j - 1, "E")):
                    g.add_edge((label(i, j - 1, "E"), label(i, j, "W")))
                if g.contains(label(i, j - 1, "W")):
                    g.add_edge((label(i, j - 1, "W"), label(i, j, "W")))

                if c == "S":
                    start = label(i, j, "E")

                if c == "E":
                    g.add_node(label(i, j, "C"))
                    for d in dirs:
                        g.add_edge(
                            (label(i, j, d), label(i, j, "C")), weight=0, directed=True
                        )
                    end = label(i, j, "C")

                # TODO: trim

    if start is None or end is None:
        raise ValueError("initialization error")

    # (b) compute shortest path
    return g.shortest_path(start, end)
