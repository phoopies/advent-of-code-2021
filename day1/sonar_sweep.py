file_name: str = "day1/sonar_sweep_input"
count = 0

def increased(a: int, b: int):
    return a < b

with open(file_name, 'r') as f:
    p = f.readline()
    prev = int(p)
    while c := f.readline():
        current = int(c)
        if increased(prev, current): count += 1
        prev = current

print(f"The depth measurement icreases {count} times")