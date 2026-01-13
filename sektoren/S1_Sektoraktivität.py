from S1_Feuerbälle import Feuerball
import random
from constants import*
import pygame

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

Feuerbaelle = []
for i in range(20):
    x = random.randint(50, WIDTH-50)
    y = random.randint(50, HEIGHT-50)
    vx = random.randint(2,5)
    vy = random.randint(2,5)
    Feuerbaelle.append(Feuerball(x, y,vx, vy))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    for b in Feuerbaelle:
        b.update()
        b.draw(screen)

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()

