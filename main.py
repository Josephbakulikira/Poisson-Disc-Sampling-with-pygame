import pygame
import math
import random
from Sample import Vector2
import colorsys

width, height = 1920, 1080
size=(width, height)
black, white, green = (10, 10, 10), (230, 230, 230), (95, 255, 1)
hue = 0

pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60

screen_offset = 2
r = 40 
k = 20

w = r/math.sqrt(2)

x = random.randint(50, width-50)
y = random.randint(50, height-50)
position = Vector2(x, y)

cl = x // w
rw = y // w
columns = width // w
rows = height // w
active_list = []

grid = [i for i in range(math.ceil(columns * rows))]

for i in range(math.ceil(columns * rows)):
    grid[i] = None
grid[math.ceil(cl+rw*columns)] = position
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    if len(active_list) > 0:
        randIndex = random.randint(0, len(active_list)-1)
        current_position = active_list[randIndex]
        found = False
        for n in range(k):
            offset = Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
            new_magnitude = random.randint(r, r*2)
            offset = offset.set_magnitude(new_magnitude)
            offset.x = offset.x + current_position.x
            offset.y = offset.y + current_position.y

            col = math.ceil(offset.x/w)
            row = math.ceil(offset.y/w)

            if row < rows-screen_offset and col < columns-screen_offset and row > screen_offset and col > screen_offset:
                checker = True
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        index = math.ceil( col + i + (row+j) * columns)

                        neighbour = grid[index];
                        if neighbour is not None:
                            dist = math.sqrt((offset.x - neighbour.x) ** 2 + (offset.y - neighbour.y) ** 2)
                            if dist < r:
                                checker = False


                if checker is True:
                    found = True
                    grid[math.ceil(col + row * columns)] = Vector2(offset.x, offset.y)
                    active_list.append(Vector2(offset.x, offset.y))
                    break
        if found is not True:
            list_splice(active_list, randIndex+1, 1)

    for cell in grid:
        if cell is not None:
            pygame.draw.circle(screen, white, (math.ceil(cell.x), math.ceil(cell.y)), 16)

    for disk in active_list:
        pygame.draw.circle(screen, hsv_to_rgb(hue, 1, 1), (math.ceil(disk.x), math.ceil(disk.y)), 16)

    pygame.display.flip()
    hue += 0.0009
pygame.quit()
