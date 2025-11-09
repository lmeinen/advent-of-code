from __future__ import annotations

import functools
import math
from typing import Generator


class Size:
    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    def range(self) -> Generator[Vec, None, None]:
        for x in range(self.rows):
            for y in range(self.cols):
                yield Vec(x, y)

    def __repr__(self):
        return f"({self.rows},{self.cols})"


@functools.total_ordering
class Vec:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def normalize(self):
        d = math.gcd(self.x, self.y)
        return self // d

    def in_range(self, size: Size) -> bool:
        return 0 <= self.x < size.rows and 0 <= self.y < size.cols

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.x < other.x if self.x != other.x else self.y < other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vec):
            return Vec(self.x * other.x, self.y * other.y)
        if isinstance(other, int):
            return Vec(self.x * other, self.y * other)
        raise NotImplementedError(f"Multiplication not defined for {type(other)}")

    def __floordiv__(self, other):
        if isinstance(other, int):
            return Vec(self.x // other, self.y // other)
        raise NotImplementedError(f"Division not defined for {type(other)}")

    def __mod__(self, other):
        if isinstance(other, Size):
            return Vec(self.x % other.cols, self.y % other.rows)
        raise NotImplementedError(f"Division not defined for {type(other)}")

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __str__(self):
        return f"({self.x},{self.y})"


class Graph:
    def __init__(self):
        self._adj = dict()

    @property
    def nodes(self) -> list[str]:
        return list(self._adj.keys())

    def contains(self, label: str) -> bool:
        """checks if the graph contains a vertex"""
        return label in self._adj

    def neighbours(self, label: str) -> list[tuple[str, int]]:
        return self._adj[label] if self.contains(label) else []

    def add_node(self, label: str) -> bool:
        """attempts to add a labeled node to the graph. Returns False iff a node with that label already exists"""
        if self.contains(label):
            return False
        else:
            self._adj[label] = []
            return True

    def add_edge(
        self, edge: tuple[str, str], weight: int = 1, directed: bool = False
    ) -> bool:
        """attempts to add an edge to the graph. Returns False iff one of the edge's nodes doesn't exist"""
        if edge[0] not in self._adj or edge[1] not in self._adj:
            return False

        self._adj[edge[0]].append((edge[1], weight))
        if not directed:
            self._adj[edge[1]].append((edge[0], weight))

        return True

    def shortest_path(self, a: str, b: str) -> int:
        """Computes the shortest path from a to b"""
        distance = {n: (0 if n == a else float('inf')) for n in self.nodes}
        unvisited = set(self.nodes)
        def smallest() -> str:
            return min(unvisited, key=lambda l: distance[l])

        while (curr := smallest()) != b:
            for (n, w) in self.neighbours(curr):
                if n in unvisited and distance[curr] + w < distance[n]:
                    distance[n] = distance[curr] + w
            unvisited.remove(curr)

        if distance[b] == float('inf'):
            raise ValueError(f"Couldn't find path from {a} to {b}")
        return int(distance[b])
