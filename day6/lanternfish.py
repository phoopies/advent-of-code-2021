from typing import List, Union

def simulate(initial_fishes: List[int], days: int):
    return sum([simulate_fish(fish, days) for fish in initial_fishes])

def simulate_fish(fish: int, days: int):
    if fish >= days: return 1 # the fish doesn't have time to reproduce, return itself
    remaining_days = days - fish - 1
    return simulate_fish(6, remaining_days) + simulate_fish(8, remaining_days) # reproduces one fish and then the remaining days for itself and the reproduced fish

def solve(filename: str = "input", days: int = 256) -> int:
    values = []
    with open(f"day6/{filename}", 'r') as f:
        line = f.readline().strip()
        values = line.split(',')
        values = [int(value) for value in values]
    fishes = simulate(values, days)
    return fishes

if __name__ == "__main__":
    result = solve("test_data")
    print(result)