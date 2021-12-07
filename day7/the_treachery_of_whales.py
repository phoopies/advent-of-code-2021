from typing import List
from math import floor

# PART 1
# The minimum distance is to the median of the points if n odd and any number between the "two median points" if even
def median(l: List[int]) -> int:
    l_new = l.copy()
    l_new.sort()
    mid = floor(len(l)/2)
    return l_new[mid]

# PART 2
# The minimun distance is propably achieved when the position is as close as possible to each point
# as that way we don't take steps that cost a lot that often
def mean(l: List[int]) -> int:
    n = len(l)
    if n == 0: return 0
    return round(sum(l) / n) 

def solve(filename: str = "input", part2: bool = True) -> int:
    values = []
    with open(f"day7/{filename}", 'r') as f:
        line = f.readline().strip()
        values = line.split(',')
        values = [int(value) for value in values]
    return solve_part2(values) if part2 else solve_part1(values)
    
def solve_part2(l: List[int]) -> int:
    close = 1
    m = mean(l)
    best = min([sum([sum([i for i in range(1, abs(value-(m+i)) + 1)]) for value in l]) for i in range(-close, close+1)]) # Check points close to mean
    return best

def solve_part1(l: List[int]) -> int: 
    m = median(l)
    return sum([abs(value-m) for value in l])

print(solve())
