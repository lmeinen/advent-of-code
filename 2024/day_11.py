from __future__ import annotations
from collections import defaultdict
from functools import cache, reduce
from itertools import accumulate, zip_longest
import math
from typing import Literal

from util.models import Coordinate, Size


def solve(part: Literal["a", "b"], input: str) -> int:
    stones: dict[int, int] = {}
    for s in [int(i) for i in input.split()]:
        stones[s] = stones.get(s, 0) + 1

    @cache
    def blink(stone: int) -> list[int]:
        if stone == 0:
            return [1]

        no_digits = int(math.log10(stone)) + 1
        if no_digits % 2 == 0:
            splitter = 10 ** (no_digits // 2)
            return [stone % splitter, stone // splitter]
        else:
            return [stone * 2024]

    for _ in range(25 if part == "a" else 75):
        nxt = {}
        for s, v in stones.items():
            for e in blink(s):
                nxt[e] = nxt.get(e, 0) + v

        stones = nxt

    return sum(stones.values())
