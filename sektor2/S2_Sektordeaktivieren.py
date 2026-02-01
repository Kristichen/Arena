import pygame
from constants import *
import os
import math


ERLOESEN_POS = (WIDTH // 3 *2, HEIGHT // 3*2)

gasmaske_img = None
gasmaske_rect = None

ICON_SIZE = (60, 60)

_active = False

def init_images():
    global gasmaske_img, gasmaske_rect

    base = os.path.dirname(__file__)
    path = os.path.join(base, "gasmaske.png")

    img = pygame.image.load(path).convert_alpha()

    if ICON_SIZE is not None:
        img = pygame.transform.smoothscale(img, ICON_SIZE)

    gasmaske_img = img
    gasmaske_rect = gasmaske_img.get_rect(center=ERLOESEN_POS)

def reset():
    global _active
    _active = True

def aktiv_machen(value: bool):
    global _active
    _active = value

def ist_active() -> bool:
    return _active

def draw(screen):
    if not _active:
        return
    if gasmaske_img is None or gasmaske_rect is None:
        return
    screen.blit(gasmaske_img, gasmaske_rect)

def touched(player) -> bool:
    if not _active:
        return False
    if gasmaske_rect is None:
        return False

    pr = PLAYER_RADIUS
    px, py = float(player.x), float(player.y)

    closest_x = max(gasmaske_rect.left, min(px, gasmaske_rect.right))
    closest_y = max(gasmaske_rect.top,  min(py, gasmaske_rect.bottom))

    dx = px - closest_x
    dy = py - closest_y
    return (dx * dx + dy * dy) <= (pr * pr)


def check_and_deactivate(player, rauch_module) -> bool:
    global _active
    if touched(player):
        rauch_module.stop()
        _active = False
        return True
    return False