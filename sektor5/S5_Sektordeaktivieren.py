import pygame
from constants import *
import os


ERLOESEN_POS = (WIDTH // 5*4, HEIGHT // 3*2)

rettungsring_img = None
rettungsring_rect = None

ICON_SIZE = (60, 60)

_active = False

def init_images():
    global rettungsring_img, rettungsring_rect

    base = os.path.dirname(__file__)
    path = os.path.join(base, "rettungsring.png")

    img = pygame.image.load(path).convert_alpha()

    if ICON_SIZE is not None:
        img = pygame.transform.smoothscale(img, ICON_SIZE)

    rettungsring_img = img
    rettungsring_rect = rettungsring_img.get_rect(center=ERLOESEN_POS)

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
    if rettungsring_img is None or rettungsring_rect is None:
        return
    screen.blit(rettungsring_img, rettungsring_rect)

def touched(player) -> bool:
    if not _active:
        return False
    if rettungsring_rect is None:
        return False

    pr = PLAYER_RADIUS
    px, py = float(player.x), float(player.y)

    closest_x = max(rettungsring_rect.left, min(px, rettungsring_rect.right))
    closest_y = max(rettungsring_rect.top,  min(py, rettungsring_rect.bottom))

    dx = px - closest_x
    dy = py - closest_y
    return (dx * dx + dy * dy) <= (pr * pr)


def check_and_deactivate(player, feuer_module) -> bool:
    global _active
    if touched(player):
        feuer_module.stop()
        _active = False
        return True
    return False