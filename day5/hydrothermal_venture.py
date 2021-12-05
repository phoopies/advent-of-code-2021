from typing import Iterable, List, Tuple, Union
import operator

class Point:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

class Line:
    def __init__(self, start: Point, end: Point, d: float = 1) -> None:
        self.line: List[Point] = self._create_line(start, end, d)
    
    def __str__(self) -> str:
        return f"[{', '.join([str(c) for c in self.line])}]"
    
    def __iter__(self) -> List[Point]:
        return iter(self.line)
    
    @property
    def max_x(self) -> int:
        if len(self.line) == 0: return
        return max([self.line[0].x, self.line[-1].x])

    @property
    def max_y(self) -> int:
        return max([self.line[0].y, self.line[-1].y])
    
    @property
    def is_diagonal(self) -> bool:
        if len(self.line) == 0: return False
        return self.line[0].x != self.line[-1].x and self.line[0].y != self.line[-1].y

    def _create_line(self, start: Point, end: Point, d: float = 1) -> List[Point]:
        x = end.x - start.x
        y = end.y - start.y

        x_dir = self._get_dir(x)
        y_dir = self._get_dir(y)

        if 0 != abs(x) != abs(y) != 0: return [start]
        points = max(abs(x), abs(y)) + 1
        return [Point(start.x + d*x_dir*dd, start.y + d*y_dir*dd) for dd in range(points)]
    
    def _get_dir(self, value: int) -> int:
        if value < 0: return -1
        if value > 0: return 1
        return 0

class Diagram:
    def __init__(self, x: int, y: int) -> None:
        self.diagram: Union[int, str] = [[0] *(x+1) for _ in range(y+1)]
    
    def __str__(self) -> str:
        return "\n".join(["".join([str(point) for point in row]) for row in self.diagram])

    def overlaps(self, atleast: int = 2) -> int:
        overlap = 0
        for row in self.diagram:
            for point in row:
                if point >= atleast: overlap += 1
        return overlap
    
    def add_line(self, line: Line, exclude_diagonals: bool = False) -> None:
        if exclude_diagonals and line.is_diagonal: return
        for point in line:
            self._add_point(point)
    
    def _add_point(self, point: Point) -> None:
        diagram_point = self.diagram[point.y][point.x]
        self.diagram[point.y][point.x] = diagram_point + 1

# def extremum(list: List[int], maximum = True) -> int:
#     ext = None
#     oper = operator.gt if maximum else operator.lt
#     for i in list:
#         if isinstance(i, list): i = max_int(i)
#         if not ext or oper(i, ext): ext = i
#     return ext

# def max_int(list: List[Line]) -> int:
#     return extremum(list)

# def min_int(list: List[Line]) -> int:
#     return extremum(list, False)

def make_point(s:str, sep = ',') -> Point:
    x, y = s.split(sep)
    return Point(int(x), int(y))

def make_line(s:str, sep = "->") -> Line:
    start_str, end_str = s.split(sep)
    start = make_point(start_str)
    end = make_point(end_str)
    return Line(start, end)

def solve(filename: str = "input", part2: bool=True) -> Tuple[int, Diagram]:
    lines = []
    max_x = 0
    max_y = 0
    with open(f"day5/{filename}", 'r') as f:
        while fl := f.readline().strip():
            line = make_line(fl)
            max_x = max(max_x, line.max_x)
            max_y = max(max_y, line.max_y)
            lines.append(line)
    diagram = Diagram(max_x, max_y)
    for line in lines:
        diagram.add_line(line, not part2)
    return diagram.overlaps(2), diagram



if __name__ == "__main__":
    # start = Point(0, 0)
    # end = Point(0, 5)
    # end2 = Point(5,0)
    # line = Line(start, end) # x = 0, y = 5
    # line2 = Line(start, end2)
    # line3 = Line(end, end2)
    # print(line)
    # print(line2)
    # print(line3)
    # diagram = Diagram(5, 5)
    # diagram.add_line(line)
    # diagram.add_line(line2)
    # print(diagram)
    result, diagram = solve("test_data")
    print(result)