from typing import List

def increased(a: List[int], b: List[int]) -> bool:
    return sum(a) < sum(b)

def sum(arr: List[int]) -> int:
    s: int = 0
    for a in arr: s += a
    return s

def next_window(arr: List[int], a: int) -> List[int]:
    new_arr: List[int] = arr.copy()
    new_arr.pop(0)
    new_arr.append(a)
    return new_arr

def solve(window_size: int = 3, file_name: str = "input") -> int:
    count: int = 0
    with open(f"day1/{file_name}", 'r') as f:
        prev = []
        for i in range(window_size):
            l = f.readline()
            prev.append(int(l))
        while c := f.readline():
            current = next_window(prev, int(c))
            if increased(prev, current): count += 1
            prev = current
    return count

file_name: str = "input"
window_size: int = 3
count = solve(window_size, file_name)

print(f"The depth measurement increases {count} times")