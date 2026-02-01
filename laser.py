import pygame
from constants import *
import math
class Laser:
    def __init__(self,start_sector, speed=0.5):
        self.angle= start_sector*60 +120
        self.speed=speed
        self.is_on= False
        self.turned_off=False

    def start(self):
        self.is_on=True
        self.turned_off=False

    def stop(self):
        self.is_on=False

    def update(self):
        if self.is_on:
            self.angle += self.speed

    def draw(self, arena):
        if not self.is_on or self.turned_off:
            return
        
        rad = math.radians(self.angle)
        x_end = CENTER[0] + math.cos(rad) * RADIUS
        y_end = CENTER[1] + math.sin(rad) * RADIUS

        pygame.draw.line(arena, "red", CENTER, (x_end, y_end),2)

    def player_hit(self, player) -> bool:
        if not self.is_on:
          return False

        rad = math.radians(self.angle)
        dx = math.cos(rad)
        dy = math.sin(rad)
        px = player.x - CENTER[0]
        py = player.y - CENTER[1]
        proj = px * dx + py * dy
        if proj <= 0:
            return False
        dist = abs(px * dy - py * dx)

        return dist <= PLAYER_RADIUS


    
    def jumped_over(self, player):
        if not self.is_on or self.turned_off:
            return False
        return not player.on_ground