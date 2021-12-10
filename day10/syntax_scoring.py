from typing import List, Tuple
from math import floor

def median(l: List[int]) -> int:
    l_new = l.copy()
    l_new.sort()
    mid = floor(len(l)/2)
    return l_new[mid]

pairs = [('(', ')'), ('[',']'), ('{','}'), ('<', '>')]
opening = list(map(lambda pair: pair[0], pairs))
closing = list(map(lambda pair: pair[1], pairs))

def get_other_pair(s: str) -> str:
    pair = list(filter(lambda p: s in p, pairs))[0]
    if s == pair[0]: return pair[1]
    return pair[0]

syntax_points = {
    ')' : (3,1),
    ']' : (57,2),
    '}' : (1197,3),
    '>' : (25137,4),
}

def find_corrupted(chunk: str) -> str: # "" if nothing uncorrupted
    stack = []
    for c in chunk:
        if c in opening: stack.append(c)
        elif c in closing:
            if (stack[-1], c) not in pairs: return c
            else: stack.pop()
        else: raise Exception(f"{c} is not a valid opening or closing symbol")
    return ""

def complete_chunk(chunk: str) -> int: # How many points it took to complete the chunk
    stack = []
    for c in chunk:
        if c in opening: stack.append(c)
        elif c in closing:
            if (stack[-1], c) not in pairs: raise Exception(f"{chunk} is corrupted can't complete it")
            stack.pop()
        else: raise Exception(f"{c} is not a valid opening or closing symbol")
    return calculate_closing_score(stack)

def calculate_closing_score(l: List[str]) -> int:
    total_score = 0
    while len(l) > 0:
        opening = l.pop()
        closing = get_other_pair(opening)
        total_score *= 5
        total_score += syntax_points[closing][1]
    return total_score

def solve(filename: str = "input") ->  Tuple[int, int]:
    points1 = 0
    points2: List[int] = []
    with open(f"day10/{filename}", 'r') as f:
        while line := f.readline().strip():
            corrupted = find_corrupted(line)
            if corrupted:
                points1 += syntax_points[corrupted][0]
            else:
                points2.append(complete_chunk(line))
    point2 = median(points2)
    return points1, point2

print(solve())
