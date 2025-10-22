from __future__ import annotations

from collections import deque
from typing import Literal

from util.models import Vec

WALL = "#"
BOX = "O"  # part a
EMPTY = "."
ROBOT = "@"
BOX_L = "["  # part b
BOX_R = "]"  # part b


def solve(part: Literal["a", "b"], input: str) -> int:

    moves, grid = parse(input, part)

    robot = None
    for x, row in enumerate(grid):
        for y, c in enumerate(row):
            if c == ROBOT:
                robot = Vec(x, y)

    if robot is None:
        raise ValueError("No robot found!")

    def get(p: Vec):
        return grid[p.x][p.y]

    def assign(p: Vec, v):
        grid[p.x][p.y] = v

    for m in moves:
        visited = []
        to_visit = deque()
        to_visit.append(robot)
        while len(to_visit) > 0:
            p = to_visit.popleft()
            if p not in visited:
                visited.append(p)
                if get(p) == WALL:
                    break
                elif get(p) != EMPTY:
                    to_visit.append(p + m)
                    if get(p + m) == BOX_L and m.y == 0:
                        to_visit.append(p + m + Vec(0, 1))
                    elif get(p + m) == BOX_R and m.y == 0:
                        to_visit.append(p + m - Vec(0, 1))
        else:
            for p in reversed(visited):
                assign(p, get(p - m) if (p - m) in visited else EMPTY)
            robot += m

    return sum(
        [
            x * 100 + y
            for x, row in enumerate(grid)
            for y, c in enumerate(row)
            if c == BOX or c == BOX_L
        ]
    )


def parse(input: str, part: Literal["a", "b"]) -> tuple[list[Vec], list[list[str]]]:

    def char_to_move(c: str) -> Vec:
        match c:
            case ">":
                return Vec(0, 1)
            case "v":
                return Vec(1, 0)
            case "<":
                return Vec(0, -1)
            case "^":
                return Vec(-1, 0)
            case _:
                raise ValueError("unknown move ", c)

    grid_input, moves = input.split("\n\n")
    moves = [char_to_move(c) for c in moves.replace("\n", "")]
    grid = [list(line) for line in grid_input.splitlines()]

    if part == "b":

        def double(c: str) -> tuple[str, str]:
            match c:
                case ".":
                    return (EMPTY, EMPTY)
                case "#":
                    return (WALL, WALL)
                case "O":
                    return (BOX_L, BOX_R)
                case "@":
                    return (ROBOT, EMPTY)
                case _:
                    raise ValueError("unknown grid value ", c)

        grid[:] = [[cc for c in row for cc in double(c)] for row in grid]

    return moves, grid
