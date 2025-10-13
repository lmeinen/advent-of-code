from collections import deque
from typing import Callable, Generator, Sequence, TypeVar

from util.models import Vec

T = TypeVar("T")


def dfs(node: T, neighbours: Callable[[T], list[T]]) -> Generator[T, None, None]:
    """returns a generator yielding nodes in DFS-order"""
    visited = set()
    S = deque()
    S.append(node)
    while len(S) > 0:
        v = S.pop()
        if not v in visited:
            visited.add(v)
            S.extend(neighbours(v))
            yield v


def bfs(node: T, neighbours: Callable[[T], list[T]]) -> Generator[T, None, None]:
    """returns a generator yielding nodes in BFS-order"""
    visited = set()
    S = deque()
    S.append(node)
    while len(S) > 0:
        v = S.popleft()
        if not v in visited:
            visited.add(v)
            S.extend(neighbours(v))
            yield v


def search(lst: Sequence[int], val: int) -> int:
    """returns insertion index for val in non-empty sorted list"""
    l = 0
    r = len(lst)
    while l < r:
        m = l + (r - l) // 2
        if lst[m] < val:
            l = m + 1
        elif lst[m] > val:
            r = m
        else:
            return m
    assert l <= r
    return l

def polygon_area(poinst: list[Vec]) -> int:
    """Computes the total area of a polygon from a list of corners in counter-clockwise order (min 3)"""
    # TODO Implement using pick's theorem or shoelace formula
    return 0