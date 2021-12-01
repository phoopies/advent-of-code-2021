from typing import List


file_name: str = "day1/sonar_sweep_input"
window_size: int = 3
count: int = 0

def increased(a: List[int], b: List[int]) -> bool:
    return sum(a) < sum(b)

def sum(arr: List[int]) -> int:
    s = 0
    for a in arr: s += a
    return s

def next_window(arr: List[int], a: int) -> List[int]:
    new_arr = arr.copy()
    new_arr.pop(0)
    new_arr.append(a)
    return new_arr

with open(file_name, 'r') as f:
    prev = []
    for i in range(window_size):
        l = f.readline()
        prev.append(int(l))
    while c := f.readline():
        current = next_window(prev, int(c))
        if increased(prev, current): count += 1
        prev = current

print(f"The depth measurement icreases {count} times")