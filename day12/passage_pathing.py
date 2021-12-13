from enum import Enum
from typing import List, Tuple


class CaveType(Enum):
    small = 's'
    big = 'B'
    start = 'start'
    end = 'end'


class Cave:
    def __init__(self, id: str) -> None:
        self.id = id
        self.type = Cave._determine_type(id)
        self.caves: List['Cave'] = []

    def __str__(self) -> str:
        return f"{self.id} {self.type} paths: " + ', '.join([cave.id for cave in self.caves])

    def add_cave(self, cave: 'Cave') -> None:
        self.caves.append(cave)

    def copy(self) -> 'Cave':
        cave_copy = Cave(self.id)
        cave_copy.caves = self.caves.copy()
        return cave_copy

    def is_small(self) -> bool:
        return self.type == CaveType.small

    def is_start(self) -> bool:
        return self.type == CaveType.start

    def is_end(self) -> bool:
        return self.type == CaveType.end

    @staticmethod
    def _determine_type(id: str) -> CaveType:
        if id == CaveType.start.value:
            return CaveType.start
        if id == CaveType.end.value:
            return CaveType.end
        if id.islower():
            return CaveType.small
        return CaveType.big


class CaveSystem:
    def __init__(self) -> None:
        self.caves: dict[str, Cave] = {}

    def add_cave(self, cave: Cave):
        if cave.id in self.caves:
            return
        self.caves[cave.id] = cave

    def __contains__(self, id: str) -> bool:
        return id in self.caves

    def __getitem__(self, id) -> Cave:
        if id in self.caves:
            return self.caves[id]
        return None

    def make_paths(self) -> int:
        start = self[CaveType.start.value].copy()
        return self._make_paths([start], False)[1]

    def _make_paths(self, current_path: List[Cave], visited_small_twice: bool) -> Tuple[List[Cave], int]:
        if current_path[-1].is_end():
            return current_path, 1  # made it to the end
        successes = 0
        for cave in current_path[-1].caves:
            if cave.is_start():
                continue
            double_visit = visited_small_twice
            if cave.id in [cave.id for cave in current_path] and cave.is_small():
                if visited_small_twice:
                    continue
                else:
                    double_visit = True
            path = current_path.copy()
            path.append(cave.copy())
            _, success = self._make_paths(path, double_visit)
            successes += success
        return current_path, successes


def solve(filename: str = "input") -> int:
    cave_system = CaveSystem()
    with open(f"day12/{filename}", 'r') as f:
        while line := f.readline().strip():
            start, end = line.split('-')
            if start not in cave_system:
                cave_system.add_cave(Cave(start))
            if end not in cave_system:
                cave_system.add_cave(Cave(end))
            cave_system[start].add_cave(cave_system[end])
            cave_system[end].add_cave(cave_system[start])
    return cave_system.make_paths()


print(solve())
