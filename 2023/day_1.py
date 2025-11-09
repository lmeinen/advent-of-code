from typing import Callable, Literal

import regex as re


def solve(part: Literal["a", "b"], input: str) -> int:
    return part_a(input) if part == "a" else part_b(input)


def solve_common(data: str, pre: Callable[[str], str]):
    val = 0
    for line in data.splitlines():
        digits = ''.join(char for char in pre(line) if char.isdigit())
        val += int(digits[0]) * 10 + int(digits[-1])
    return val


def part_a(data: str):
    return solve_common(data, lambda s: s)


def part_b(data: str):
    m = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    p = "|".join("({})".format(key) for key, _ in m.items())

    def pre(s: str) -> str:
        matches = re.finditer(p, s, overlapped=True)
        r = ""
        idx = 0
        for match in matches:
            r += s[idx : match.start()] + m[match.group(0)]
            idx = match.end()
        r += s[idx:]
        return r

    return solve_common(
        data,
        pre,
    )
