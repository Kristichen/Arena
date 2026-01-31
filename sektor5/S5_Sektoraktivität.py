import pygame
import math

from constants import PLAYER_RADIUS
from sektor5.S5_Wasser import Wasserball

from sektor5 import S5_Wasser
def init_images():
    S5_Wasser.init_images()

_wasserbälle = []
_is_running = False
_start_tick = 0

WASSER_POS = [
    (425, 700),
    (350, 550),
    (200, 300),
    (550, 450),
    (500, 250),
    (700, 250),
    (250, 500),
    (675, 675),
]
WASSER_ZEITEN_MS = [0, 0, 3000, 6000, 9000, 12000, 14000, 16000]

def start():
    global _wasserbälle, _is_running, _start_tick
    _is_running = True
    _start_tick = pygame.time.get_ticks()
    _wasserbälle = [None] * len(WASSER_ZEITEN_MS)


def stop():
    global _wasserbälle, _is_running
    _is_running = False
    _wasserbälle = []

def player_hit(player) -> bool:
    if not _is_running:
        return False

    px, py = float(player.x), float(player.y)
    pr = PLAYER_RADIUS

    for bälle in _wasserbälle:
        if bälle is None:
            continue

        for x, y, size in bälle.layers:
            rr = size / 2
            if math.hypot(px - x, py - y) <= pr + rr:
                return True

    return False


def update_and_draw(screen):
    if not _is_running:
        return

    now = pygame.time.get_ticks() - _start_tick

    for i in range(len(_wasserbälle)):
        if _wasserbälle[i] is None and now >= WASSER_ZEITEN_MS[i]:
            x, y = WASSER_POS[i]
            _wasserbälle[i] = Wasserball(x, y)

    for bälle in _wasserbälle:
        if bälle is None:
            continue
        bälle.update()
        bälle.draw(screen)