import pygame
import math

from constants import PLAYER_RADIUS
from sektor_2.S2_Gas import RauchWolke

from sektor_2 import S2_Gas
def init_images():
    S2_Gas.init_images()

_rauchwolken = []
_is_running = False
_start_tick = 0

RAUCH_POS = [
    (425, 700),
    (350, 550),
    (200, 300),
    (550, 450),
    (500, 250),
    (700, 250),
    (250, 500),
    (675, 675),
]
RAUCH_ZEITEN_MS = [0, 0, 3000, 6000, 9000, 12000, 14000, 16000]

def start():
    global _rauchwolken, _is_running, _start_tick
    _is_running = True
    _start_tick = pygame.time.get_ticks()
    _rauchwolken = [None] * len(RAUCH_ZEITEN_MS)


def stop():
    global _rauchwolken, _is_running
    _is_running = False
    _rauchwolken = []

def player_hit(player) -> bool:
    if not _is_running:
        return False

    px, py = float(player.x), float(player.y)
    pr = PLAYER_RADIUS

    for wolke in _rauchwolken:
        if wolke is None:
            continue

        for x, y, size in wolke.layers:
            rr = size / 2
            if math.hypot(px - x, py - y) <= pr + rr:
                return True

    return False


def update_and_draw(screen):
    if not _is_running:
        return

    now = pygame.time.get_ticks() - _start_tick

    for i in range(len(_rauchwolken)):
        if _rauchwolken[i] is None and now >= RAUCH_ZEITEN_MS[i]:
            x, y = RAUCH_POS[i]
            _rauchwolken[i] = RauchWolke(x, y)

    for wolke in _rauchwolken:
        if wolke is None:
            continue
        wolke.update()
        wolke.draw(screen)