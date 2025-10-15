from __future__ import annotations

import re
from functools import reduce
from typing import Literal

from util.algs import crt
from util.models import Size, Vec


def solve(part: Literal["a", "b"], input: str) -> int:

    lines = input.splitlines()
    size = Size(7, 11) if len(lines) <= 12 else Size(103, 101)
    robots = []

    for l in lines:
        if m := re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", l):
            p = Vec(int(m.group(1)), int(m.group(2)))
            v = Vec(int(m.group(3)), int(m.group(4)))
            robots.append((p, v))

    return safety(quadrants(robots, size)) if part == "a" else solve_b(robots, size)


def quadrants(
    robots: list[tuple[Vec, Vec]], size: Size, seconds: int = 100
) -> list[int]:
    quadrants = [0] * 4
    middle_column = size.cols // 2 + 1
    middle_row = size.rows // 2 + 1
    for p, v in robots:
        final_position = walk(size, p, v, seconds)
        if not (
            final_position.x + 1 == middle_column or final_position.y + 1 == middle_row
        ):
            quadrants[
                (final_position.x + 1) // middle_column
                + 2 * ((final_position.y + 1) // middle_row)
            ] += 1

    return quadrants


def safety(quadrants):
    return reduce(lambda x, y: x * y, quadrants, 1)


def solve_b(robots: list[tuple[Vec, Vec]], size: Size) -> int:
    if len(robots) < 50:
        # example is somehow parsed incorrectly
        return 0

    # (a) low safety factor implies a low standard deviation
    # (b) horizontal patterns repeat every 101 cycles, vertical every 103
    # (c) using CRT, we can find s such that both patterns occur at once - likely resulting in a christmas tree
    sf = [quadrants(robots, size, s) for s in range(size.cols)]
    s1, s2 = sorted(range(len(sf)), key=lambda i: safety(sf[i]))[:2]
    if (len(robots) // 4 < sf[s1][0] and len(robots) // 4 < sf[s1][2]) or (
        len(robots) // 4 < sf[s1][1] and len(robots) // 4 < sf[s1][3]
    ):
        ax = s1
        ay = s2
    else:
        ax = s2
        ay = s1

    return crt(ax, ay, size.cols, size.rows)


def walk(size, p, v, seconds):
    return (p + v * seconds) % size
