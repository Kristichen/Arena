import pygame
from constants import *
import math

class Laser:
    def __init__(self,start_sector, speed=0.1):
        self.angle= start_sector*60 +30
        self.speed=speed
        self.is_on= True
    def update(self):
        if self.is_on:
            self.angle += self.speed
    def draw(self, arena):
        if not self.is_on:
            return
        
        rad = math.radians(self.angle)
        x_end = CENTER[0] + math.cos(rad) * RADIUS
        y_end = CENTER[1] + math.sin(rad) * RADIUS

        pygame.draw.line(arena, "red", CENTER, (x_end, y_end),2)
