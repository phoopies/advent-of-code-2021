from functools import reduce
from typing import List, Tuple
from time import time


class Area:
    def __init__(self, heightmap: List[List[int]] = []) -> None:
        self.heightmap = heightmap

    def __str__(self) -> str:
        return str(self.heightmap)

    def append(self, row: List[int]) -> None:
        self.heightmap.append(row)

    def find_low_points(self) -> List[int]:
        low_points = []
        for y in range(len(self.heightmap)):
            for x in range(len(self.heightmap[y])):
                if self.is_low_point(x, y):
                    low_points.append(self.heightmap[y][x])
        return low_points

    def is_low_point(self, x: int, y: int) -> bool:
        point = self.heightmap[y][x]
        to_compare_with = []
        if y - 1 >= 0:
            to_compare_with.append(self.heightmap[y-1][x])
        if y + 1 < len(self.heightmap):
            to_compare_with.append(self.heightmap[y+1][x])
        if x - 1 >= 0:
            to_compare_with.append(self.heightmap[y][x-1])
        if x + 1 < len(self.heightmap[y]):
            to_compare_with.append(self.heightmap[y][x+1])
        return all([point < compare for compare in to_compare_with])

    # Return the product of the sizes of the largers basins
    def find_largest_basins(self, count: int = 3) -> int:
        border_map = [[[0, 0] for _ in row] for row in self.heightmap]
        i = 1
        for y in range(len(self.heightmap)):  # Mark all independent rows
            for x in range(len(self.heightmap[y])):
                if self.heightmap[y][x] == 9:
                    i += 1
                else:
                    border_map[y][x][0] = i
            i += 1

        for x in range(len(self.heightmap[0])):  # Mark all independent columns
            for y in range(len(self.heightmap)):
                if self.heightmap[y][x] == 9:
                    i += 1
                else:
                    border_map[y][x][1] = i
            i += 1

        basins: List[List[set, int]] = []  # area, count
        for row in border_map:  # Go through marked rows and columns and combine them
            for x, y in row:
                if x == 0 == y:
                    continue
                overlaps = list(
                    filter(lambda basin: x in basin[0] or y in basin[0], basins))
                n = len(overlaps)
                if n == 1:  # Add the new point to the overlapping
                    overlaps[0][0].add(x)
                    overlaps[0][0].add(y)
                    overlaps[0][1] += 1
                elif n > 1:  # Add new point and combine overlapping areas
                    for i in range(1, n):
                        overlaps[0][1] += overlaps[i][1] + 1
                        overlaps[0][0] = overlaps[0][0].union(overlaps[i][0])
                        basins.remove(overlaps[i])
                else:
                    # Create a new area with that point
                    basins.append([set([x, y]), 1])
        counts = sorted([basin[1] for basin in basins], reverse=True)
        biggest = counts[:count]
        return reduce(lambda x, y: x * y, biggest, 1)


def solve(filename: str = "input") -> Tuple[int, int]:
    area = Area([])
    with open(f"day9/{filename}", 'r') as f:
        while line := f.readline().strip():
            values = [int(v) for v in line]
            area.append(values)
    return sum([point + 1 for point in area.find_low_points()]), area.find_largest_basins(3)


print(solve("test_data"))

# start = time()
# for _ in range(10):
#     solve()
# end = time()
# print(f"Took {end-start} seconds")
