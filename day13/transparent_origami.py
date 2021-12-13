from typing import List, Tuple, Union

Fold = Tuple[int, bool]
Point = Tuple[int, int]


class Paper:
    def __init__(self, length: int, height: int) -> None:
        self.paper: List[str] = [
            ['.' for _ in range(length+1)] for _ in range(height+1)]

    def __str__(self) -> str:
        return "\n".join([''.join(row) for row in self.paper])

    def add(self, points: Union[Point, List[Point]]) -> None:
        if not isinstance(points, list):
            points = [points]
        for point in points:
            self.paper[point[1]][point[0]] = '#'

    def fold(self, split: int, horizontal: bool) -> None:
        n = len(self.paper) if not horizontal else len(self.paper[0])
        for i in range(split):
            for d in range(n):
                r = (2 * split) - i
                if horizontal:
                    if r >= len(self.paper):
                        break
                    if self.paper[r][d] == '#':
                        self.paper[i][d] = '#'
                else:
                    if r >= len(self.paper[d]):
                        break
                    if self.paper[d][r] == '#':
                        self.paper[d][i] = '#'
        if horizontal:
            self.paper = self.paper[:split]
        else:
            self.paper = [[point for x, point in enumerate(
                row) if x < split] for row in self.paper]

    def dot_count(self) -> int:
        return sum(map(len, [list(filter(lambda p: p == '#', row)) for row in self.paper]))


def solve(filename: str = "input") -> Tuple[Paper, int]:
    points: List[Point] = []
    folds: List[Fold] = []
    length = 0
    height = 0
    with open(f"day13/{filename}", 'r') as f:
        while line := f.readline().strip():  # Get the points
            x, y = line.split(',')
            points.append((x := int(x), y := int(y)))
            if x > length:
                length = x
            if y > height:
                height = y
        while line := f.readline().strip():  # Get the folds
            inst = line.split(' ')[2]
            x_or_y, value = inst.split('=')
            horizontal = x_or_y == 'y'
            folds.append((int(value), horizontal))
    paper = Paper(length, height)
    paper.add(points)
    for fold in folds:
        paper.fold(fold[0], fold[1])
    return paper, paper.dot_count()


paper, dots = solve()
print(paper)
print(dots)
