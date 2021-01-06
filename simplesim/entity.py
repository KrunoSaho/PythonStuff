from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from util import sign_int
import random


@dataclass
class Point:
    x: int
    y: int
    z: int

    @staticmethod
    def make_random(range_a: int, range_b: int):
        make_point = lambda: random.randint(range_a, range_b)
        return Point(make_point(), make_point(), make_point())

    def distance(self, other: Point) -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5

    def replace_coord(self, k, n):
        coords = (self.x, self.y, self.z)
        if k <= 0:
            coords = (n, self.y, self.z)
        elif k <= 1:
            coords = (self.x, n, self.z)
        else:
            coords = (self.x, self.y, n)
        return Point(*coords)

    def delta(self, other: Point) -> Point:
        sx = sign_int(self.x - other.x)
        sy = sign_int(self.y - other.y)
        sz = sign_int(self.z - other.z)
        return Point(sx, sy, sz)

    def __add__(self, other: Point):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)


@dataclass
class Entity:
    id: int
    coords: Point

    def distance(self, other: Entity) -> float:
        dx = self.coords.x - other.coords.x
        dy = self.coords.y - other.coords.y
        dz = self.coords.z - other.coords.z
        return (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5


class EntityManager:
    entities: list[Entity]

    def __init__(self) -> None:
        super().__init__()
        self.entities = []

    def find(self, coords: Point) -> Optional[Entity]:
        es = [e for e in self.entities if e.coords == coords]
        return None if len(es) == 0 else es[0]

    def set_dimension_values(self, dimen_value: list[tuple[int, int]]):
        def setval(entities: list[Entity]):
            for e in entities:
                for k, n in dimen_value:
                    e.coords = e.coords.replace_coord(k, n)
                yield e

        self.entities = list(setval(self.entities))

    def generate_random(self, n: int):
        entities = [Entity(id, Point.make_random(-100, 100)) for id in range(n)]
        self.entities.extend(entities)

    def shuffle(self):
        random.shuffle(self.entities)

    def sort_by_distance(self, starting_point: Point = Point(0, 0, 0)):
        entities = self.entities
        entities_with_dist = [(starting_point.distance(a.coords), a) for a in entities]
        self.entities = [x for _, x in sorted(entities_with_dist, key=lambda x: x[0])]

    def get_ids(self):
        return [e.id for e in self.entities]