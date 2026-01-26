import pygame
import math
import time
from constants import *
from laser import Laser

import random

from player import Player

WIDTH, HEIGHT = 900, 900
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 350
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
arena=pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Fate of Nature: Survive the Arena")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 48)

# Farben
SECTOR_COLORS = [
    (120 ,220 ,200 ),      # türkis hell [0]
    ( 40,130 ,120 ),    # türkis dunkel [1]
    (80 ,110 ,170 ),      # marine hell [2]
    (20 ,40 ,90 ),    # marine dunkel [3]
    (120, 200,120 ),    # grün hell [4]
    (40 ,120 ,60 ),    # grün dunkel [5]
]

current_sector = 0  
sector_aktiv = [False, False, False, False, False, False]

COUNTDOWN_TIME = 20  
sector_end_time = time.time() + COUNTDOWN_TIME

def sektort_von_position(pos):
    dx = pos[0] - CENTER[0]
    dy = pos [1] - CENTER[1]
    distance = math.sqrt(dx*dx + dy * dy)

    if distance >= RADIUS:
        return None
    
    winkel = (math.degrees(math.atan2(dy,dx)) + 360) % 360
    return int(winkel // 60)

def draw_sector(screen, mitte, radius, winkel_start, winkel_ende, color):
    points = [mitte]
    step = 2
    for angle in range(winkel_start, winkel_ende + 1, step):
        rad = math.radians(angle) # von CHATGPT ERKLàRT
        x = mitte[0] + radius * math.cos(rad) # von CHATGPT ERKLàRT
        y = mitte[1] + radius * math.sin(rad) # von CHATGPT ERKLàRT
        points.append((x, y))
    pygame.draw.polygon(screen, color, points)


running = True
player=Player(WIDTH/2,HEIGHT/2,4,4)
laser=Laser(start_sector=1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    time_left = int(sector_end_time - time.time())

    if time_left <= 0:
        current_sector = (current_sector + 1) % 6
        sector_end_time = time.time() + COUNTDOWN_TIME
        time_left = COUNTDOWN_TIME
    screen.fill((240, 230, 200))

    pressed = pygame.key.get_pressed()
    player.update(pressed)
    laser.update()

    pygame.draw.circle(arena, (120, 80, 40), CENTER, RADIUS + 5)
    pygame.draw.circle(arena, (240, 240, 240), CENTER, RADIUS)

        # Aktiven Sektor färben
    start = current_sector * 60
    ende = start + 60
    draw_sector(arena, CENTER, RADIUS, start, ende, SECTOR_COLORS[current_sector])

    laser.draw(arena)

    text_countdown = font.render(f"Countdown: {time_left}s", True, (0, 0, 0))
    screen.blit(text_countdown, (WIDTH - 300, 30))

    text_sector = font.render(f"Aktiver Sektor: {current_sector + 1}", True, (0, 0, 0))
    screen.blit(text_sector, (WIDTH - 320, 80))
    

    zoom = player.get_zoom()
    scaled_w = int(WIDTH * zoom)
    scaled_h = int(HEIGHT * zoom)
    scaled_arena = pygame.transform.smoothscale(arena, (scaled_w, scaled_h))

    arena_x = (WIDTH - scaled_w) // 2
    arena_y = (HEIGHT - scaled_h) // 2

    screen.blit(scaled_arena, (arena_x, arena_y)) 

    player.draw(screen)
    



    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()