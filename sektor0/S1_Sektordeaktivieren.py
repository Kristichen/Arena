import pygame
from constants import *
import os

# Erlösen-Kreis (in der Mitte)
ERLOESEN_POS = (WIDTH // 3, HEIGHT // 3)

feuerloescher_img = None
feuerloescher_rect = None

ICON_SIZE = (60, 60)

def init_images():
    global feuerloescher_img, feuerloescher_rect

    base = os.path.dirname(__file__)
    path = os.path.join(base, "feuerloescher.png")

    img = pygame.image.load(path).convert_alpha()

    if ICON_SIZE is not None:
        img = pygame.transform.smoothscale(img, ICON_SIZE)

    feuerloescher_img = img
    feuerloescher_rect = feuerloescher_img.get_rect(center=ERLOESEN_POS)

def draw(screen):
    if feuerloescher_img is None or feuerloescher_rect is None:
        return
    screen.blit(feuerloescher_img, feuerloescher_rect)

def touched(player) -> bool:
    if feuerloescher_rect is None:
        return False

    pr = PLAYER_RADIUS

    px, py = float(player.x), float(player.y)
    closest_x = max(feuerloescher_rect.left, min(px, feuerloescher_rect.right))
    closest_y = max(feuerloescher_rect.top,  min(py, feuerloescher_rect.bottom))

    dx = px - closest_x
    dy = py - closest_y
    return (dx*dx + dy*dy) <= (pr * pr)


def check_and_deactivate(player, feuer_module) -> bool:
    if touched(player):
        feuer_module.stop()
        return True
    return False