from enum import Enum
from typing import List, Tuple



class Direction(Enum):
    FORWARD: Tuple[int] = (1,0)
    UP: Tuple[int] = (0,1)
    DOWN: Tuple[int] = (0, -1)

class Position:
    def __init__(self) -> None:
        self.horizontal: int = 0
        self.depth: int = 0
        self.aim: int = 0
    
    def __str__(self) -> str:
        return f"x: {self.horizontal}\ty: {self.depth}"
    
    def move(self, direction: Direction, amount: int) -> None:
        self.horizontal += direction.value[0] * amount
        self.depth += direction.value[0] * self.aim * amount
        self.aim -= direction.value[1] * amount
    
    def move_str(self, s: str) -> None:
        arr = s.split()
        if len(arr) != 2: return
        direction_str, amount_str = arr
        direction = Direction[direction_str.upper()]
        if not amount_str.isdigit(): return
        amount = int(amount_str)
        self.move(direction, amount)
    
    def product(self) -> int:
        return self.horizontal * self.depth

def solve(filename: str = "input") -> Tuple[int, Position]:
    pos: Position = Position()
    with open(f"day2/input", 'r') as f:
        while c := f.readline():
            pos.move_str(c)
    return pos.product(), pos

solution, pos  = solve()
print(pos)
print(solution)
