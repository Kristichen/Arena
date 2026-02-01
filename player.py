import pygame
from constants import *
from math import sqrt
import os

class Player:
    def __init__(self, x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.on_ground=True
        self.jump_height = 0
        self.alive = True

        base = os.path.dirname(__file__)
        path = os.path.join(base, "mädchen.png")

        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2)
        )

        self.rect = self.image.get_rect(center=(self.x, self.y))
    def draw (self, screen):
            self.rect.center = (int(self.x), int(self.y))
            screen.blit(self.image, self.rect)

    def update(self, pressed):
        if not self.alive:
            return
        new_x=self.x
        new_y=self.y

        if pressed[pygame.K_UP]:
            new_y -= self.vy
        if pressed[pygame.K_DOWN]:
            new_y += self.vy
        if pressed[pygame.K_LEFT]:
            new_x -= self.vx
        if pressed[pygame.K_RIGHT]:
            new_x += self.vx

        dx = new_x-WIDTH/2
        dy = new_y-HEIGHT/2
        radii=RADIUS-PLAYER_RADIUS

        if sqrt(dx**2 +dy**2)<radii:
            self.x= new_x
            self.y= new_y

        if pressed[pygame.K_SPACE] and self.on_ground:
            self.on_ground=False
            self.jump_height=20

        if not self.on_ground:
            self.jump_height -= 0.75
            if self.jump_height <= 0:
                self.jump_height = 0
                self.on_ground = True

    def get_zoom(self):
        return 1 - self.jump_height * 0.005
    