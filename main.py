# Example file showing a basic pygame "game loop"

import pygame
from constants import *

import random

from player import Player
# pygame setup
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fate of Nature: Survive the Arena")
clock = pygame.time.Clock()
running = True
player=Player(100,100,4,4)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed = pygame.key.get_pressed()
    screen.fill("black")
    player.update(pressed)

    arena=pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    cx, cy = WIDTH // 2, HEIGHT // 2
    pygame.draw.circle(arena, "darkgreen", (cx, cy), ARENA_RADIUS)
    

    zoom = player.get_zoom()
    scaled_w = int(WIDTH * zoom)
    scaled_h = int(HEIGHT * zoom)
    scaled_arena = pygame.transform.smoothscale(arena, (scaled_w, scaled_h))

    arena_x = (WIDTH - scaled_w) // 2
    arena_y = (HEIGHT - scaled_h) // 2

    screen.fill("black")
    screen.blit(scaled_arena, (arena_x, arena_y)) 

    player.draw(screen)
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()