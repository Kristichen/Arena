import pygame
import random
import math
from constants import *
import os


class Bomb:
    def __init__(self):
        self.image = pygame.image.load("Bilder/bomb.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        
        self.expl_img = pygame.image.load("bilder/expl.png").convert_alpha()
        self.expl_img = pygame.transform.scale(self.expl_img, (160, 160))

        self.pos=self.random_position()
        self.rect=self.image.get_rect(center=self.pos)
        self.time= pygame.time.get_ticks()
        self.explode_time= 3000
        self.expl_rad=80

        self.exploded= False
        self.defused=False

        self.expl_end=0
        self.expl_time=1000

    def random_position(self):
        while True:
            x= random.randint(CENTER[0]-ARENA_RADIUS +80, CENTER[0]+ARENA_RADIUS -80)
            y= random.randint(CENTER[1]-ARENA_RADIUS +80, CENTER[1]+ARENA_RADIUS -80)
            dx= x - CENTER[0]
            dy= y - CENTER[1]
            distance= math.sqrt(dx*dx + dy*dy)
            if distance <= ARENA_RADIUS -80:
                return (x,y)
            
    def update(self):
        if self.defused:
            return
        if not self.exploded:
            current_time= pygame.time.get_ticks()
            if current_time - self.time >= self.explode_time:
                self.exploded= True 
                self.expl_end= current_time + self.expl_time
        else:
            if pygame.time.get_ticks() > self.expl_end:
                self.defused= True
                self.exploded= False
    def draw(self, arena):
        if self.defused:
            return
        arena.blit(self.image, self.rect)
        if self.exploded:
            explosion_rect = self.expl_img.get_rect(center=self.pos)
            arena.blit(self.expl_img, explosion_rect)


    def player_hit(self,player):
        if not self.exploded:
            return False
        dx= player.x - self.pos[0]
        dy= player.y - self.pos[1]
        distance= math.sqrt(dx*dx + dy*dy)
        return distance <= self.expl_rad + PLAYER_RADIUS
    
    def defuse(self, player):
        if self.exploded:
            return
        dx= player.x - self.pos[0]
        dy= player.y - self.pos[1]
        distance= math.sqrt(dx*dx + dy*dy)
        if distance <= PLAYER_RADIUS +20:
            self.defused= True   
            return True
        return False      