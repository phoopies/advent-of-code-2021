from typing import List
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
                if self.is_low_point(x,y): low_points.append(self.heightmap[y][x])
        return low_points

    def is_low_point(self, x: int, y: int) -> bool:
        point = self.heightmap[y][x]
        to_compare_with = []
        if y - 1 >= 0: to_compare_with.append(self.heightmap[y-1][x])
        if y + 1 < len(self.heightmap): to_compare_with.append(self.heightmap[y+1][x])
        if x - 1 >= 0: to_compare_with.append(self.heightmap[y][x-1])
        if x + 1 < len(self.heightmap[y]): to_compare_with.append(self.heightmap[y][x+1])
        return all([point < compare for compare in to_compare_with])



def solve(filename: str = "input"):
    area = Area()
    with open(f"day9/{filename}", 'r') as f:
        while line := f.readline().strip():
            values = [int(v) for v in line]
            area.append(values)
    return sum([point + 1 for point in area.find_low_points()])
        
print(solve())        

start = time()
for i in range(100):
    print(i)
    solve()
end = time()
print(f"Took {end-start} seconds")