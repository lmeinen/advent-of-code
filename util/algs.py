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


def batch(iterable, n=1):
    """itertools.batch is not yet available in python 3.11"""
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx : min(ndx + n, l)]

def crt(a1: int, a2: int, n1: int, n2: int) -> int:
    """Solves the system x === a1 (mod m1) x === a2 (mod m2) for x, assuming m1 and m2 are coprime"""
    r, m1, m2 = egcd(n1, n2)
    assert r == 1, "moduli given to CRT are not coprime"
    x = a1 * m2 * n2 + a2 * m1 * n1
    return (x) % (n1 * n2)



def egcd(a, b):
    """Extended euclidian algorithm to compute gcd(a,b), and integers s, t such that s*a+t*b=gcd(a,b)"""
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        q, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    assert old_r == old_s * a + old_t * b

    return old_r, old_s, old_t


def det(a: Vec, b: Vec) -> int:
    """determinant of 2x2 matrix M = a | b"""
    return a.x * b.y - b.x * a.y


def polygon_area(poinst: list[Vec]) -> int:
    """Computes the total area of a polygon from a list of corners in counter-clockwise order (min 3)"""
    # TODO Implement using pick's theorem or shoelace formula
    return 0
