from typing import List, Tuple, Union


class Octopus:
    flash_level: int = 9
    def __init__(self, energy_level: int) -> None:
        self.resting = False
        self.energy_level = energy_level
    
    def __str__(self) -> str:
        return str(self.energy_level)

    def take_step(self, count: int = 1) -> bool:
        if self.resting or count == 0: return False
        self.energy_level += count
        if self.energy_level > Octopus.flash_level:
            self.resting = True
            self.energy_level = 0
            return True
        return False
    
    def rested(self) -> None:
        self.resting = False


class Octopi:
    def __init__(self, octopi: Union[List[List[int]], List[List[Octopus]]] = []) -> None:
        if not octopi: self.octopi = octopi
        elif isinstance(octopi, list) and len(octopi) > 0 and isinstance(octopi[0], list) and len(octopi[0]) > 0:
            if isinstance(octopi[0][0], int): 
                self.octopi = [[Octopus(i) for i in row] for row in octopi]
            elif isinstance(octopi[0][0], Octopus):
                self.octopi = octopi
            else: raise Exception(f"Invalid argument. {type(octopi[0][0])} is not a valid type for octopi")
        else: raise Exception("Invalid argument")
    
    def append(self, octopi: Union[List[int], List[Octopus]]) -> None:
        if isinstance(octopi[0], int):
            self.octopi.append([Octopus(i) for i in octopi])
        else :self.octopi.append(octopi)


    def get_surrounding(self, x: int, y: int) -> List[Tuple[int,int]]:
        octopi = []
        # print(x,y)
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == dy == 0: continue
                if 0 <= y + dy < len(self.octopi):
                    if 0 <= x + dx < len(self.octopi[y + dy]):
                        octopi.append((y+dy, x+dx))
        return octopi
    
    def simulate(self, days: int = 100) -> Tuple[int, int]:
        flashes = 0
        flashes_now = 0
        n_octopi = len(self.octopi) * len(self.octopi[0])
        day = 0
        while flashes_now != n_octopi:
            day += 1
            flashes_now = self._simulate_step()
            if day <= days: flashes += flashes_now
        return flashes, day

    
    def _simulate_step(self) -> int:
        flashes = 0
        flashed = [[pus.take_step() for pus in row] for row in self.octopi]
        while any(map(any, flashed)):
            to_flash = [[0 for _ in row] for row in flashed]
            for y, row in enumerate(flashed):
                for x, flash in enumerate(row):
                    if flash:
                        flashes += 1
                        flashed[y][x] = 0
                        octopi = self.get_surrounding(x, y)
                        for ny, nx in octopi:
                            to_flash[ny][nx] += 1
            flashed = [[pus.take_step(flash) for (pus, flash) in zip(row, frow)] for (row, frow) in zip(self.octopi, to_flash)]
        self._rested()
        return flashes
    
    def _rested(self) -> None:
        for row in self.octopi:
            for pus in row:
                pus.rested()
    
    def __str__(self) -> str:
        return "\n".join([" ".join([str(pus) for pus in row]) for row in self.octopi])


def solve(filename: str = "input") ->  Tuple[int, int]:
    octopi = Octopi([])
    with open(f"day11/{filename}", 'r') as f:
        while line := f.readline().strip():
            values = [int(v) for v in line]
            octopi.append(values)
    flashes, first_simultaneous = octopi.simulate(100)
    return flashes, first_simultaneous

if __name__ == "__main__":
    # test = [
    #     [1,1,1,1,1],
    #     [1,9,9,9,1],
    #     [1,9,1,9,1],
    #     [1,9,9,9,1],
    #     [1,1,1,1,1],
    # ]

    # group = [[Octopus(x) for x in row] for row in test]
    # octopi = Octopi(group)
    # print(octopi.simulate(2))
    # print(octopi)

    print(solve())