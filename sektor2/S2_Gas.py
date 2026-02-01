import pygame
import random
import math
from constants import CENTER, ARENA_RADIUS
import os


rauch_img = None

def init_images():
    global rauch_img
    base = os.path.dirname(__file__)
    rauch_img = pygame.image.load(os.path.join(base, "rauchball.png")).convert_alpha()

def bleibt_in_arena(x, y, size):
    cx, cy = CENTER
    max_dist = ARENA_RADIUS - size // 2
    dx = x - cx
    dy = y - cy
    dist = math.hypot(dx, dy)

    if dist > max_dist:
        scale = max_dist / dist
        x = cx + dx * scale
        y = cy + dy * scale

    return x, y

class RauchWolke:
    def __init__(self, x, y):
        x, y = bleibt_in_arena(x, y, 30)
        self.layers = [(x, y, 30)]  
        self.start_tick = pygame.time.get_ticks()
        self.spawn_index = 0

        times = [1.0]
        t = 3.0
        while t <= 20.0:
            times += [t, t + 1, t + 2]
            t += 5.0
        self.spawn_times_ms = [int(s * 1000) for s in times if s <= 20.0]

    def update(self):
        now = pygame.time.get_ticks() - self.start_tick
        while self.spawn_index < len(self.spawn_times_ms) and now >= self.spawn_times_ms[self.spawn_index]:
            self.spawn_one()
            self.spawn_index += 1

    def spawn_one(self):
        ax, ay, asize = random.choice(self.layers)
        new_size = random.randint(25, 40)  

        r_prev = asize / 2
        r_new = new_size / 2

        overlap = new_size / 5  

        distance = (r_prev + r_new) - overlap
        if distance < 2:
            distance = 2

        angle = random.uniform(0, 2 * math.pi)
        nx = ax + math.cos(angle) * distance
        ny = ay + math.sin(angle) * distance

        nx, ny = bleibt_in_arena(nx, ny, new_size)
        self.layers.append((nx, ny, new_size))

    def draw(self, surface):
        for x, y, size in self.layers:
            img = pygame.transform.scale(rauch_img, (size, size))  
            rect = img.get_rect(center=(int(x), int(y)))
            surface.blit(img, rect)

