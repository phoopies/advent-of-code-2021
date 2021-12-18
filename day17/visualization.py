import matplotlib.pyplot as plt 
from typing import List, Tuple
from matplotlib.animation import FuncAnimation, PillowWriter

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

    def shoot_until(self, x_vel: int, y_vel: int, target: Trench) -> Tuple[bool, List[Tuple[int, int]]]:
        self.set_velocity(x_vel, y_vel)
        y_low = min(target.y)
        x_max = max(target.x)
        projectory = [(self.x, self.y)]
        while not target.inside(self.x, self.y):
            projectory.append(self.step())
            if self.y < y_low or self.x > x_max:
                return False, projectory
        return True, projectory

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

    def possible_shots(self) -> List[List[Tuple[int, int]]]:
        min_x = self.slow_shot()
        max_x = self.fast_shot()
        min_y = self.low_shot()
        max_y = self.high_shot()

        shots = []
        probe = Probe()
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                success, projectory = probe.shoot_until(x,y, self.target)
                if success:
                    shots.append(projectory)
                probe.reset()
        return shots

    def shoot(self, x_vel: int, y_vel: int, steps: int) -> bool:
        probe = Probe()
        projectory = probe.shoot(x_vel, y_vel, steps)
        print(projectory)
        return any([point in self.target for point in projectory])

import random
def new_color():
    r,g,b = random.random(),random.random(),random.random()
    return [r,g,b]

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'o')

test_target = Trench(20, -10, 30, -5)
real_target = Trench(207, -115, 263, -63)
target = real_target
 
from matplotlib.patches import Rectangle
rectangle_anchor = (min(target.x), min(target.y))
rectangle_width = max(target.x) - min(target.x)
rectangle_height = max(target.y) - min(target.y)
ax.add_patch(Rectangle(rectangle_anchor, rectangle_width, rectangle_height ,color="green", alpha=.20))

launcher = Launcher(target)
shots = launcher.possible_shots()
print(len(shots))
xs = [x for shot in shots for [x, _y] in shot]
ys = [y for shot in shots for [_x, y] in shot]
frame = list(zip(xs, ys))
def update(i):
    global ln, xdata, ydata, ax, frame
    x, y = frame[i]
    if x == 0 == y:
        color = new_color()
        xdata, ydata = [], []
        ln, = plt.plot(xdata, ydata, 'o', c=color)
    xdata.append(x)
    ydata.append(y)
    ln.set_data(xdata, ydata)

    return ln, 

def init():
    ax.set_xlim(-3, max(target.x) + 3)
    ax.set_ylim(min(target.y)-3, launcher.high_shot()+3)
    return ln,

ani = FuncAnimation(fig, update, frames=len(xs),
            init_func=init, interval=3, blit=True, repeat=True)

ani.save('day17/visualization.gif', dpi=300, fps=12)