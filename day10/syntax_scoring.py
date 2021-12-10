pairs = [('(', ')'), ('[',']'), ('{','}'), ('<', '>')]

syntax_points = {
    '' : 0,
    ')' : 3,
    ']' : 57,
    '}' : 1197,
    '>' : 25137,
}

def find_corrupted(chunk: str) -> str: # "" if nothing uncorrupted
    stack = []
    opening = list(map(lambda pair: pair[0], pairs))
    closing = list(map(lambda pair: pair[1], pairs))
    for c in chunk:
        if c in opening: stack.append(c)
        elif c in closing:
            if (stack[-1], c) not in pairs: return c
            else: stack.pop()
        else: raise Exception(f"{c} is not a valid opening or closing symbol")
    return ""

def solve(filename: str = "input") ->  int:
    points = 0
    with open(f"day10/{filename}", 'r') as f:
        while line := f.readline().strip():
            corrupted = find_corrupted(line)
            points += syntax_points[corrupted]
    return points

print(solve())
