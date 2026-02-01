from sektor0.S1_Feuerbälle import*
from constants import * 
import random
from constants import PLAYER_RADIUS
from player import*

_feuerbaelle = [] # _ -> damit interne Liste
_is_spaming = False

def start(anzahl = 20):
    global _feuerbaelle, _is_spaming
    _is_spaming = True
    _feuerbaelle = []

    for _ in range(anzahl):
        vx = random.uniform(0.5,2)
        vy = random.uniform(0.5,2)
        _feuerbaelle.append(Feuerball(punkte,vx, vy))

def stop():
    global _feuerbaelle, _is_spaming
    _is_spaming = False
    _feuerbaelle = []

def player_hit(player) -> bool:

        px, py = float(player.x), float(player.y)
        pr = PLAYER_RADIUS

        for b in _feuerbaelle:
            if not b.alive:
                continue
            dx = px - b.x
            dy = py - b.y
            dist = math.hypot(dx, dy)
            if dist <= pr + b.radius:
                return True

        return False

def update_and_draw(screen):
    if not _feuerbaelle:
        return
    for b in _feuerbaelle:
        b.update()
        b.draw(screen)

