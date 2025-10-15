from __future__ import annotations

import re
from math import gcd
from typing import Literal

from util.algs import batch, det
from util.models import Vec


def solve(part: Literal["a", "b"], input: str) -> int:
    total = 0
    for b in batch(input.splitlines(), 4):
        if (
            (ma := re.match(r"Button [A|B]: X\+(\d+), Y\+(\d+)", b[0]))
            and (mb := re.match(r"Button [A|B]: X\+(\d+), Y\+(\d+)", b[1]))
            and (mp := re.match(r"Prize: X=(\d+), Y=(\d+)", b[2]))
        ):
            a = Vec(int(ma.group(1)), int(ma.group(2)))
            b = Vec(int(mb.group(1)), int(mb.group(2)))
            p = Vec(int(mp.group(1)), int(mp.group(2)))
            if part == "b":
                p += Vec(10000000000000, 10000000000000)
        else:
            raise ValueError(f"input didn't match format: {b}")

        no_a = None
        no_b = None
        if det(a, b) != 0:
            # A and B are linearly independent: apply cramer's rule
            if det(p, b) % det(a, b) == 0 and det(a, p) % det(a, b) == 0:
                # we only consider integer solutions
                no_a = det(p, b) // det(a, b)
                no_b = det(a, p) // det(a, b)
        elif det(a, p) == 0 and p.x % gcd(a.x, b.x) == 0 and p.y % gcd(a.y, b.y) == 0:
            # A and B are linearly dependent and an integer solution (x, y) exist
            # NOTE: other solutions exist of the form (x + kv, y - ku), where k is an arbitrary integer, and u and v are the quotients of a and b w.r.t. gcd
            print(f"found linearly dependent buttons {a} and {b}")
            
        if no_a and no_b and (part != "a" or (no_a <= 100 and no_b <= 100)):
            total += no_a * 3 + no_b

    return total

