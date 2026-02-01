import pygame
import math
from constants import *

ERLOESEN_POS = (WIDTH // 2, HEIGHT // 2)
ERLOESEN_RADIUS = 22

ERLOESEN_COLOR = (255, 165, 0)
ERLOESEN_BORDER = (200, 120, 0)    

def draw(screen):
    pygame.draw.circle(screen, ERLOESEN_COLOR, ERLOESEN_POS, ERLOESEN_RADIUS)
    pygame.draw.circle(screen, ERLOESEN_BORDER, ERLOESEN_POS, ERLOESEN_RADIUS, 3)

def touched(player) -> bool:
    pr = PLAYER_RADIUS  

    dx = float(player.x) - ERLOESEN_POS[0]
    dy = float(player.y) - ERLOESEN_POS[1]
    dist = math.hypot(dx, dy)

    return dist <= (ERLOESEN_RADIUS + pr)


def check_and_deactivate(player, feuer_module) -> bool:
    if touched(player):
        feuer_module.stop()
        return True
    return False