import pygame
import math
import os
import random
from constants import CENTER, ARENA_RADIUS, WIDTH, HEIGHT

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spielarena mit Countdown und Sektoren")
clock = pygame.time.Clock()

riss1_img = None
riss2_img = None

def init_images():
    global riss1_img, riss2_img
    base = os.path.dirname(__file__)
    riss1_img = pygame.image.load(os.path.join(base, "risse1.png")).convert_alpha()
    riss2_img = pygame.image.load(os.path.join(base, "risse2.png")).convert_alpha()

def punkte_auf_Kreisbogen(cx, cy, r, deg_start, deg_end, step_deg=1):
    pts = []
    deg_start %= 360
    deg_end %= 360

    if deg_start <= deg_end:
        degrees = range(deg_start, deg_end + 1, step_deg)
    else:
        degrees = list(range(deg_start, 360, step_deg)) + list(range(0, deg_end + 1, step_deg))

    for d in degrees:
        w = math.radians(d)
        x = cx + r * math.cos(w)
        y = cy + r * math.sin(w)
        pts.append((x, y))
    return pts

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

class Risse:
    def __init__(self, x, y):
        x, y = bleibt_in_arena(x, y, 30)
        self.layers = [(x, y, 30)]  # Startwolke (x, y, size)
        self.start_tick = pygame.time.get_ticks()
        self.spawn_index = 0

    def draw(self, surface):
        for x, y, size in self.layers:
            img = pygame.transform.scale(riss1_img, (size, size))  
            rect = img.get_rect(center=(int(x), int(y)))
            surface.blit(img, rect)



screen.fill((240, 230, 200))
pygame.draw.circle(screen, (120, 80, 40), CENTER, ARENA_RADIUS + 5)
pygame.draw.circle(screen, (240, 240, 240), CENTER, ARENA_RADIUS)

