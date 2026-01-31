from turtle import distance
import pygame

from constants import *
import math

class Laser:
    def __init__(self,start_sector, speed=0.1):
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
        if not self.is_on or self.turned_off:
            return False

        rad = math.radians(self.angle)
        x1, y1 = CENTER
        x2 = CENTER[0] + math.cos(rad) * RADIUS
        y2 = CENTER[1] + math.sin(rad) * RADIUS
        px, py = player.x, player.y

        num = abs((y2 - y1)*px - (x2 - x1)*py + x2*y1 - y2*x1)
        den = math.hypot(y2 - y1, x2 - x1)

        distance = num / den if den != 0 else 999
        return distance < PLAYER_RADIUS
    
    def jumped_over(self, player):
        if not self.is_on or self.turned_off:
            return False
        return not player.on_ground and player.jump_height > 10