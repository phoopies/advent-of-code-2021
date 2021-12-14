from typing import List, Tuple, Union
import pygame
from math import floor

square_size = 70
tick_speed = 55
black = [0, 0, 0]
white = [255, 255, 255]
done = False

class Octopus:
    flash_level: int = 9
    phases = [(255-i,)*3 for i in range(0, 255, floor(256/flash_level) - 1)]

    def __init__(self, scr: pygame.Surface, energy_level: int, pos: Tuple[int, int] = (0, 0)) -> None:
        self.scr = scr
        self.resting = False
        self.energy_level = energy_level
        self.pos = pos
        self.phase = Octopus.phases[self.energy_level]
        self.update()

    def __str__(self) -> str:
        return str(self.energy_level)

    def take_step(self, count: int = 1) -> bool:
        if self.resting or count == 0:
            return False
        self.energy_level += count
        if self.energy_level > Octopus.flash_level:
            self.flash()
            return True
        self.update()
        return False

    def update(self) -> None:
        self.phase = Octopus.phases[self.energy_level]
        pygame.draw.rect(self.scr, self.phase, pygame.Rect(
            self.pos[0]*square_size, self.pos[1]*square_size, square_size, square_size))

    def flash(self) -> None:
        # TODO FLASH
        self.resting = True
        self.energy_level = 0
        self.update()

    def rested(self) -> None:
        self.resting = False


class Octopi:
    def __init__(self, scr: pygame.Surface, octopi: Union[List[List[int]], List[List[Octopus]]] = []) -> None:
        self.scr = scr
        if not octopi:
            self.octopi = octopi
        elif isinstance(octopi, list) and len(octopi) > 0 and isinstance(octopi[0], list) and len(octopi[0]) > 0:
            if isinstance(octopi[0][0], int):
                self.octopi = [[Octopus(self.scr, i, (x, y)) for x, i in enumerate(
                    row)] for y, row in enumerate(octopi)]
            elif isinstance(octopi[0][0], Octopus):
                self.octopi = octopi
            else:
                raise Exception(
                    f"Invalid argument. {type(octopi[0][0])} is not a valid type for octopi")
        else:
            raise Exception("Invalid argument")

    def append(self, octopi: Union[List[int], List[Octopus]]) -> None:
        if isinstance(octopi[0], int):
            y = len(self.octopi)
            self.octopi.append([Octopus(self.scr, i, (x, y))
                               for x, i in enumerate(octopi)])
        else:
            self.octopi.append(octopi)

    def get_surrounding(self, x: int, y: int) -> List[Tuple[int, int]]:
        octopi = []
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == dy == 0:
                    continue
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
            try_quit()
            if done: break
            day += 1
            flashes_now = self._simulate_step()
            if day <= days:
                flashes += flashes_now
        return flashes, day

    def _simulate_step(self) -> int:
        clock = pygame.time.Clock()
        flashes = 0
        flashed = [[pus.take_step() for pus in row] for row in self.octopi]
        clock.tick(tick_speed)
        pygame.display.flip()
        while any(map(any, flashed)):
            try_quit()
            if done: break
            to_flash = [[0 for _ in row] for row in flashed]
            for y, row in enumerate(flashed):
                for x, flash in enumerate(row):
                    if flash:
                        flashes += 1
                        flashed[y][x] = 0
                        octopi = self.get_surrounding(x, y)
                        for ny, nx in octopi:
                            to_flash[ny][nx] += 1
            flashed = [[pus.take_step(flash) for (pus, flash) in zip(
                row, frow)] for (row, frow) in zip(self.octopi, to_flash)]
            clock.tick(tick_speed)
            pygame.display.flip()
        self._rested()
        pygame.display.flip()
        return flashes

    def _rested(self) -> None:
        for row in self.octopi:
            for pus in row:
                pus.rested()

    def __str__(self) -> str:
        return "\n".join([" ".join([str(pus) for pus in row]) for row in self.octopi])


def try_quit() -> bool:
    global done
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            return True


if __name__ == "__main__":

    filename = "input"
    values = []

    with open(f"day11/{filename}", 'r') as f:
        while line := f.readline().strip():
            values.append([int(v) for v in line])

    done = False
    width = len(values[0])
    height = len(values)

    print(width)

    pygame.init()

    scr = pygame.display.set_mode((width * square_size, height * square_size))
    scr.fill(black)

    pygame.display.set_caption("Animation")
    octopi = Octopi(scr, values)
    pygame.display.flip()

    input("start")
    octopi.simulate(100)
    if not done: input("exit")

    pygame.quit()
