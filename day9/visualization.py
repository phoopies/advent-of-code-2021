from functools import reduce
from typing import List, Tuple
import pygame
import random

def random_color() -> List[int]:
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

def triangle(x: int, y: int, size: int, upper: bool) -> List[List[int]]:
    x_scaled = x*square_size
    y_scaled = y*square_size
    left_top_corner = [x_scaled,y_scaled]
    right_bottom_corner = [x_scaled+size-1, y_scaled+size-1]
    third_corner = [x_scaled+size-1, y_scaled] if upper else [x_scaled, y_scaled+size-1]
    return [left_top_corner, right_bottom_corner, third_corner]

def try_quit() -> bool:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  
            return True

if __name__ == "__main__":
    area = []
    black = [0, 0, 0]
    white = [255, 255, 255]
    tick_speed = 2500
    filename = "input"
    with open(f"day9/{filename}", 'r') as f:
        while line := f.readline().strip():
            values = [int(v) for v in line]
            area.append(values)
    square_size = 12
    width = len(area[0]) 
    height = len(area)

    pygame.init()

    scr = pygame.display.set_mode((width * square_size, height * square_size))
    pygame.display.set_caption("Animation")

    clock = pygame.time.Clock()
    done = False 

    scr.fill(white)

    border_map = [[[0, 0] for _ in row] for row in area]
    colors = [[ [white, white] for _ in row] for row in area]
    for y in range(len(area)):
        for x in range(len(area[y])):
            if area[y][x] == 9: 
                pygame.draw.rect(scr, black, [x*square_size, y*square_size, square_size, square_size])
                colors[y][x] = [[ [black, black] for _ in row] for row in area]
    pygame.display.flip()

    input("start")

    i = 1
    color = random_color()
    for y in range(len(area)):  # Mark all independent rows
        if try_quit(): done = True
        if done: break
        for x in range(len(area[y])):
            if try_quit(): done = True
            if done: break
            if area[y][x] == 9:
                i += 1
                color = random_color()
            else:
                pygame.draw.polygon(scr, color, triangle(x, y, square_size, True))
                border_map[y][x][0] = i
                colors[y][x][0] = color
                pygame.display.flip()
                clock.tick(tick_speed)
        i += 1
        color = random_color()

    for x in range(len(area[0])):  # Mark all independent columns
        if try_quit(): done = True
        if done: break
        for y in range(len(area)):
            if try_quit(): done = True
            if done: break
            if area[y][x] == 9:
                i += 1
                color = random_color()
            else:
                border_map[y][x][1] = i
                pygame.draw.polygon(scr, color, triangle(x, y, square_size, False))
                colors[y][x][1] = color
                pygame.display.flip()
                clock.tick(tick_speed)
        i += 1
        color = random_color()
        
    Comb = Tuple[set[int], int, List[int], set[Tuple[int, int]]] # area, count, color, positions
    basins: List[Comb] = []  

    for dy, row in enumerate(border_map):  # Go through marked rows and columns and combine them
        if done: break
        for dx, (x, y) in enumerate(row):
            if try_quit():
                done = True
            if done: break
            if x == 0 == y:
                continue
            overlaps = list(
                filter(lambda basin: x in basin[0] or y in basin[0], basins))
            n = len(overlaps)
            if n >= 1:  # Add the new point to the overlapping
                overlaps[0][0].add(x)
                overlaps[0][0].add(y)
                overlaps[0][1] += 1
                overlaps[0][3].add((dx, dy))
                pygame.draw.rect(scr, overlaps[0][2], pygame.Rect(dx*square_size, dy*square_size, square_size, square_size))
                if n > 1:  # combine overlapping areas
                    for k in range(1, n):
                        overlap = overlaps[k]
                        overlaps[0][0] = overlaps[0][0].union(overlap[0])
                        overlaps[0][1] += overlap[1] + 1   
                        for ddx, ddy in overlap[3]:
                            overlaps[0][3].add((ddx, ddy))
                            pygame.draw.rect(scr, overlaps[0][2], pygame.Rect(ddx*square_size, ddy*square_size, square_size, square_size))
                            pygame.display.flip()
                            clock.tick(tick_speed)
                        basins.remove(overlap)
            else:
                # Create a new area with that point
                color = colors[dy][dx][0]
                basins.append([set([x, y]), 1, color, set([(dx, dy)])])
                pygame.draw.rect(scr, color, pygame.Rect(dx*square_size, dy*square_size, square_size, square_size))
            pygame.display.flip()
            clock.tick(tick_speed)

    pygame.display.flip()
    if not done: input("exit")
    pygame.quit()
