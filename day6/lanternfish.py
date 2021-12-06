from typing import List

def simulate(initial_values: List[int], days: int = 256, days_to_reproduce: int = 6, days_to_reproduce_first_time: int = 8) -> int:
    fishes = [0] * (days_to_reproduce_first_time + 1)
    for initial_value in initial_values: fishes[initial_value] += 1
    for _day in range(days):
        to_reproduce = fishes[0]
        for i in range(0, days_to_reproduce_first_time):
            fishes[i] = fishes[i+1]
        fishes[-1] = 0
        fishes[days_to_reproduce] += to_reproduce
        fishes[days_to_reproduce_first_time] += to_reproduce
    return sum(fishes)

def solve(filename: str = "input", days: int = 256) -> int:
    values = []
    with open(f"day6/{filename}", 'r') as f:
        line = f.readline().strip()
        values = line.split(',')
        values = [int(value) for value in values]
    fishes = simulate(values, days)
    return fishes

if __name__ == "__main__":
    result = solve()
    print(result)