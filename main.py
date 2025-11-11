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
    player.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()