from sektoren.S1_Feuerbälle import*
from constants import * 
import random
from constants import PLAYER_RADIUS
from player import*
#import pygame

_feuerbaelle = [] # _ -> damit interne Liste
_is_running = False
#_bleibende = False

def start(anzahl = 20):
    global _feuerbaelle, _is_running
    _is_running = True
    #_bleibende = False
    _feuerbaelle = []

    for _ in range(anzahl):
        vx = random.uniform(0.5,2)
        vy = random.uniform(0.5,2)
        _feuerbaelle.append(Feuerball(punkte,vx, vy))

#def bleibendebälle_aktivieren():
 #   global _bleibende, _is_running
  #  _bleibende = True
   # _is_running = True

#def is_bleibende():
#    return _bleibende

#def get_balls():
 #   return _feuerbaelle

def stop():
    global _feuerbaelle, _is_running
    _is_running = False
    #_bleibende = False 
    _feuerbaelle = []

def player_hit(player) -> bool:
        if not _is_running:
            return False

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
    if not _is_running:
        return
    
    for b in _feuerbaelle:
        b.update()
        b.draw(screen)

