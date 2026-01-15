from sektoren.S1_Feuerbälle import*
from constants import * 
import random
#import pygame

_feuerbaelle = [] # _ -> damit interne Liste
_is_running = False

def start(anzahl = 20):
    global _feuerbaelle, _is_running
    _is_running = True
    _feuerbaelle = []

    for _ in range(anzahl):
        x = random.randint(50, WIDTH-50)
        y = random.randint(50, HEIGHT-50)
        vx = random.uniform(0.5,2)
        vy = random.uniform(0.5,2)
        _feuerbaelle.append(Feuerball(x, y,vx, vy))

def stop():
    global _feuerbaelle, _is_running
    _is_running = False
    _feuerbaelle = []

def update_and_draw(screen):
    if not _is_running:
        return
    
    for b in _feuerbaelle:
        b.update()
        b.draw(screen)

