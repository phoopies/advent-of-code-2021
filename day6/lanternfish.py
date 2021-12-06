from typing import List, Union


class LanternFish:
    def __init__(self, initial_value: int = 8) -> None:
        self.value = initial_value
    
    def next_day(self) -> Union[None, 'LanternFish']:
        self.value -= 1
        return self._reproduce()
    
    def _reproduce(self) -> Union[None, 'LanternFish']:
        if self.value < 0: 
            self.value = 6
            return LanternFish()
        return None

def simulate(fishes: List[LanternFish], days: int) -> List[LanternFish]:
    for _day in range(days):
        new_borns = []
        for fish in fishes:
            if new_born := fish.next_day(): new_borns.append(new_born)
        for new_born in new_borns: fishes.append(new_born)
    return fishes

def make_fishes(l: List[int]) -> List[LanternFish]:
    return list(map(lambda x: LanternFish(x), l))

def solve(filename: str = "input", days: int = 80) -> int:
    fishes = []
    with open(f"day6/{filename}", 'r') as f:
        line = f.readline().strip()
        values = line.split(',')
        values = [int(value) for value in values]
        fishes = make_fishes(values)
    after = simulate(fishes, days)
    print([a.value for a in after])
    return len(after)


result = solve()
print(result)