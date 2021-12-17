from typing import List, Tuple


'''
PART 1

Conservation of energy / momentum -> there exists some y != start_y so that y == start_y (== 0)
Now we wan't the last step to be as big as possible -> y = - y_low, assuming y_low <= 0
now realizing that with max height shot we take the same amount of steps from y_start to y_top
as from y_top to y (== 0)

-> return sum([i for i in range(1, -1*(lowest_y)])
'''


class Trench:
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.x = (x1, x2)
        self.y = (y1, y2)

    def __contains__(self, point: Tuple[int, int]) -> bool:
        return self.inside(point[0], point[1])

    def inside(self, x: int, y: int) -> bool:
        return self.inside_x(x) and self.inside_y(y)

    def inside_x(self, x: int) -> bool:
        return self.x[0] <= x <= self.x[1]

    def inside_y(self, y: int) -> bool:
        return self.y[0] <= y <= self.y[1]


class Probe:
    drag: int = 1
    gravity: int = -1

    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.x_vel = 0
        self.y_vel = 0

    def set_velocity_x(self, vel: int) -> None:
        self.x_vel = vel

    def set_velocity_y(self, vel: int) -> None:
        self.y_vel = vel

    def set_velocity(self, vel_x: int, vel_y: int) -> None:
        self.set_velocity_x(vel_x)
        self.set_velocity_y(vel_y)

    def handle_gravity(self) -> None:
        self.set_velocity_y(self.y_vel + Probe.gravity)

    def handle_drag(self) -> None:
        direction = 0
        if self.x_vel > 0:
            direction = -Probe.drag
        elif self.x_vel < 0:
            direction = Probe.drag
        self.set_velocity_x(self.x_vel + direction)

    def step(self) -> Tuple[int, int]:
        self.x += self.x_vel
        self.y += self.y_vel
        self.handle_gravity()
        self.handle_drag()
        return self.x, self.y

    def shoot(self, x_vel: int, y_vel: int, steps: int = 100) -> List[Tuple[int, int]]:
        self.set_velocity(x_vel, y_vel)
        projectory = [self.step() for _ in range(steps)]
        return projectory

    def shoot_until(self, x_vel: int, y_vel: int, target: Trench) -> bool:
        self.set_velocity(x_vel, y_vel)
        y_low = min(target.y)
        x_max = max(target.x)
        while not target.inside(self.x, self.y):
            self.step()
            if self.y < y_low or self.x > x_max:
                return False
        return True

    def reset(self) -> None:
        self.x = 0
        self.y = 0


class Launcher:
    def __init__(self, target: Trench) -> None:
        self.target = target

    def high_shot(self) -> int:
        return sum([i for i in range(1, -1*(min(self.target.y)))])

    def low_shot(self) -> int:
        return min(self.target.y)

    def fast_shot(self) -> int:
        return max(self.target.x)

    def slow_shot(self) -> int:
        x_vel = 1
        while not self.target.inside_x(sum([i for i in range(1, x_vel+1)])):
            x_vel += 1
        return x_vel

    def possible_shots(self) -> int:
        min_x = self.slow_shot()
        max_x = self.fast_shot()
        min_y = self.low_shot()
        max_y = self.high_shot()

        shots = 0
        probe = Probe()
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                if probe.shoot_until(x, y, self.target):
                    shots += 1
                probe.reset()
        return shots

    def shoot(self, x_vel: int, y_vel: int, steps: int) -> bool:
        probe = Probe()
        projectory = probe.shoot(x_vel, y_vel, steps)
        print(projectory)
        return any([point in self.target for point in projectory])


def solve(filename: str = "input") -> Tuple[int, int]:
    x1, x2, y1, y2 = 0, 0, 0, 0
    with open(f"day17/{filename}", 'r') as f:
        line = f.readline().strip()
        line = line.replace("target area: ", "")
        xs, ys = [s[2:] for s in line.split(", ")]
        x1, x2 = [int(x) for x in xs.split('..')]
        y1, y2 = [int(y) for y in ys.split('..')]
    target = Trench(x1, y1, x2, y2)
    launcher = Launcher(target)
    return launcher.high_shot(), launcher.possible_shots()


if __name__ == "__main__":
    # test_target = Trench(20, -10, 30, -5)
    # real_target = Trench(207, -115, 263, -63)
    # from time import time
    # s = time()
    # launcher = Launcher(real_target)
    # print(launcher.possible_shots())
    # e = time()
    # print(e-s)
    print(solve())
