from typing import List
from math import floor
# The minimum distance is to the median of the points if n odd and any number between the "two median points" if even

def median(l: List[int]) -> int:
    l_new = l.copy()
    l_new.sort()
    mid = floor(len(l)/2)
    return l_new[mid]

def solve(filename: str = "input") -> int:
    values = []
    with open(f"day7/{filename}", 'r') as f:
        line = f.readline().strip()
        values = line.split(',')
        values = [int(value) for value in values]
    med = median(values)
    return sum([abs(value-med) for value in values])


print(solve("input"))
