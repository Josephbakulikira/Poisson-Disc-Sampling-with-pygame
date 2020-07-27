import pygame
import os
import math
import random
from disc import Disc
import colorsys

os.environ["SDL_VIDEO_CENTERED"]='1'

width, height = 1920, 1080
size=(width, height)
black, white, green = (10, 10, 10), (230, 230, 230), (95, 255, 1)
hue = 0
pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60

r = 40
k = 30

w = r/math.sqrt(2)

x = random.randint(50, width-50)
y = random.randint(50, height-50)
position = Disc(x, y)

cl = math.floor(x/w)
rw = math.floor(y/w)
columns = math.floor(width/w)
rows = math.floor(height/w)
active_list = []
grid = [i for i in range(math.floor(columns * rows))]
for i in range(math.floor(columns * rows)):
    grid[i] = None
grid[math.floor(cl+rw*columns)] = position
active_list.append(position)

def list_splice(target, start, delete_count=None, *items):
    if delete_count == None:
        delete_count = len(target) - start

    total = start + delete_count
    removed = target[start:total]
    target[start:total] = items
    return removed

def hsv_to_rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

run = True
while run:
    clock.tick(fps)
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if len(active_list) > 0:
        randIndex = random.randint(0, len(active_list)-1)
        current_position = active_list[randIndex]
        found = False
        for n in range(k):
            x_offset = random.uniform(-1, 1)
            y_offset = random.uniform(-1, 1)
            magnitude = math.sqrt(x_offset * x_offset + y_offset * y_offset)
            new_magnitude = random.randint(r, r*2)
            normal_vx = x_offset /magnitude
            normal_vy = y_offset /magnitude
            vx = normal_vx * new_magnitude
            vy = normal_vy * new_magnitude
            vx += current_position.x
            vy += current_position.y

            col = math.floor(vx/w)
            row = math.floor(vy/w)

            if row < rows and col < columns and row > 0 and col > 0:
                checker = True
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        index = math.floor( col + i + (row+j) * columns)
                        if index <= len(grid)-1:
                            neighbour = grid[index];
                            if neighbour is not None:
                                dist = math.sqrt((vx - neighbour.x) ** 2 + (vy - neighbour.y) ** 2)
                                if dist < r:
                                    checker = False
                        else:
                            checker = False

                if checker is True:
                    found = True
                    grid[math.floor(col + row * columns)] = Disc(vx, vy)
                    active_list.append(Disc(vx, vy))
                    break
        if found is not True:
            list_splice(active_list, randIndex+1, 1)

    for cell in grid:
        if cell is not None:
            pygame.draw.circle(screen, white, (math.floor(cell.x), math.floor(cell.y)), 16)
    for disk in active_list:
        pygame.draw.circle(screen, hsv_to_rgb(hue, 1, 1), (math.floor(disk.x), math.floor(disk.y)), 16)
    pygame.display.update()
    hue += 0.0009
pygame.quit()
