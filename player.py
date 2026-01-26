import pygame
from constants import *
from math import sqrt

class Player:
    def __init__(self, x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.on_ground=True
        self.jump_height = 0
        self.alive = True

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.x, self.y), PLAYER_RADIUS)

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

        dx=new_x-WIDTH/2
        dy=new_y-HEIGHT/2
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
    