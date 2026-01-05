import pygame
from constants import *

class Player:
    def __init__(self, x,y,vx,vy):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.on_the_ground=True
        self.jump_height = 0

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
            self.on_the_ground=False
            self.jump_height=20

        if not self.on_the_ground:
            self.jump_height -= 1
            if self.jump_height <= 0:
                self.jump_height = 0
                self.on_the_ground = True

    def get_zoom(self):
        """
        Returns zoom factor based on how high the jump is.
        0 → no zoom, 20 → small zoom-out
        """
        return 1 - self.jump_height * 0.005
