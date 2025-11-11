import pygame
from constants import *

class Player:
    def __init__(self, x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.on_the_ground=True
        self.jump=0
        self.gravity = 1

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.x, self.y), 10)

    def update(self, pressed):
        if pressed[pygame.K_UP]:
            self.y -= self.vy
        if pressed[pygame.K_DOWN]:
            self.y += self.vy
        if pressed[pygame.K_LEFT]:
            self.x -= self.vx
        if pressed[pygame.K_RIGHT]:
            self.x += self.vx

        if pressed[pygame.K_SPACE] and self.on_the_ground:
            self.jump=-15
            self.on_the_ground=False
