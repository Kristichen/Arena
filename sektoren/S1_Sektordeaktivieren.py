import pygame
import math
from constants import *

# Erlösen-Kreis (in der Mitte)
ERLOESEN_POS = (WIDTH // 2, HEIGHT // 2)
ERLOESEN_RADIUS = 22

ERLOESEN_COLOR = (220, 50, 50)      # rot
ERLOESEN_BORDER = (120, 20, 20)     # dunkler Rand


def draw(screen):
    """Zeichnet den roten Erlösen-Kreis."""
    pygame.draw.circle(screen, ERLOESEN_COLOR, ERLOESEN_POS, ERLOESEN_RADIUS)
    pygame.draw.circle(screen, ERLOESEN_BORDER, ERLOESEN_POS, ERLOESEN_RADIUS, 3)


def touched(player) -> bool:
    """True, wenn Player den Erlösen-Kreis berührt."""
    # Player-Radius: nimm deine Konstante
    pr = PLAYER_RADIUS  # falls deine Konstante anders heisst: anpassen!

    dx = float(player.x) - ERLOESEN_POS[0]
    dy = float(player.y) - ERLOESEN_POS[1]
    dist = math.hypot(dx, dy)

    return dist <= (ERLOESEN_RADIUS + pr)


def check_and_deactivate(player, sektor1_module) -> bool:
    """
    Wenn berührt -> sektor1.stop() (Feuerbälle weg).
    Gibt True zurück, wenn deaktiviert wurde.
    """
    if touched(player):
        sektor1_module.stop()
        return True
    return False