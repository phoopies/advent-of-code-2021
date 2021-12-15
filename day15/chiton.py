from typing import List


class Cavern:
    def __init__(self, risk_map: List[int], expansion: int = 5) -> None:
        self.map = self.expand(risk_map, expansion)
        self.risks = [[0 for _ in row] for row in self.map]

    def expand(self, risk_map: List[List[int]], times: int = 5) -> List[List[int]]:
        def add(a: int, b: int, loop: int = 9) -> int:
            return (a + b - 1) % loop + 1

        yn = len(risk_map)
        xn = len(risk_map[0])
        expanded = [[0 for _ in range(times*xn)] for _row in range(times*yn)]

        for y, row in enumerate(risk_map):
            for x, value in enumerate(row):
                for i in range(times):
                    v = add(value, i)
                    expanded[y][x + i*xn] = v
        for x in range(xn*times):
            for y in range(yn):
                for i in range(times):
                    value = expanded[y][x]
                    v = add(value, i)
                    expanded[y + (i*yn)][x] = v
        return expanded

    def calculate_risks(self, first: bool = False) -> None:
        changed = False
        xn = len(self.map[0])
        yn = len(self.map)
        for y, row in enumerate(self.map):
            for x, risk in enumerate(row):
                if x == 0 == y:
                    continue
                points = [(y + dy, x + dx) for (dy, dx) in [(0, -1), (0, 1),
                                                            (1, 0), (-1, 0)] if 0 <= y + dy < yn and 0 <= x + dx < xn]
                if first:
                    points = list(
                        filter(lambda p: self.risks[p[0]][p[1]] != 0, points))
                if not points:
                    self.risks[y][x] = risk
                    changed = True
                else:
                    point = min(points, key=lambda p: self.risks[p[0]][p[1]])
                    new = self.risks[point[0]][point[1]] + risk
                    if new != self.risks[y][x]:
                        changed = True
                        self.risks[y][x] = new
        if changed:
            self.calculate_risks()

    def lowest_risk(self) -> int:
        return self.risks[-1][-1]


def solve(filename: str = "input") -> int:
    risk_map = []
    with open(f"day15/{filename}", 'r') as f:
        while line := f.readline().strip():
            risk_map.append([int(v) for v in line])
    cavern = Cavern(risk_map, 5)
    cavern.calculate_risks(True)
    return cavern.lowest_risk()

print(solve())
