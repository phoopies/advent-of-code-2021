from typing import List, Tuple

class Cavern:
    def __init__(self, risk_map: List[int]) -> None:
        self.map = risk_map
        self.risks = [[0 for _ in row] for row in risk_map]
        self.xn = len(self.risks[0])
        self.yn = len(self.risks)
        self.calculate_risks(True)

        
    def calculate_risks(self, first: bool = False) -> None: 
        changed = False
        for y, row in enumerate(self.map):
            for x, risk in enumerate(row):
                if x == 0 == y: continue
                points = [(y + dy,x + dx) for (dy, dx) in [(0,-1), (0, 1), (1,0), (-1,0)] if 0 <= y + dy < self.yn and 0 <= x + dx < self.xn]
                if first: points = list(filter(lambda p: self.risks[p[0]][p[1]] != 0, points))
                if not points: 
                    self.risks[y][x] = risk
                    changed = True 
                else:
                    point = min(points, key= lambda p: self.risks[p[0]][p[1]])
                    new = self.risks[point[0]][point[1]] + risk
                    if new != self.risks[y][x]:
                        changed = True
                        self.risks[y][x] = new
        if changed: self.calculate_risks()
  
    def lowest_risk(self) -> int:
        return self.risks[-1][-1]

def solve(filename: str = "input") -> int:
    risk_map = []
    with open(f"day15/{filename}", 'r') as f:
        while line := f.readline().strip(): 
            risk_map.append([int(v) for v in line])
    cavern = Cavern(risk_map)
    return cavern.lowest_risk()


# test = [
#     [0, 1, 1, 9, 9],
#     [9, 9, 1, 9, 9],
#     [1, 1, 1, 9, 9],
#     [9, 2, 9, 9, 9],
#     [1, 1, 1, 1, 1]
# ]
# cavern = Cavern(test)
# print(cavern.lowest_risk())
print(solve())