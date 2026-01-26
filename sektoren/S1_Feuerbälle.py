import pygame
from constants import *
import math
import random

cx, cy = WIDTH//2, HEIGHT//2
r = ARENA_RADIUS

punkte = []
for i in range(210, 271):
    w = math.radians(i)
    x = cx + r * math.cos(w)
    y = cy + r * math.sin(w)
    punkte.append((x, y))

class Feuerball:
    def __init__(self, punkte, vx, vy):
        x, y = random.choice(punkte)

        self.radius = 5
        self.alive = True
        self.color = (255, 165, 0) 

        dx = x - cx
        dy = y - cy
        dist = math.hypot(dx, dy)

        push_in = self.radius + 6 

        if dist != 0:
            x = cx + (dx / dist) * (r - push_in)
            y = cy + (dy / dist) * (r - push_in)

        self.x = float(x)
        self.y = float(y)

        self.vx = float(vx)
        self.vy = float(vy)


    def update(self):
        if not self.alive:
            return 
        
        self.x += self.vx
        self.y += self.vy

        dx = self.x - cx
        dy = self.y - cy 
        dist = math.hypot(dx, dy)

        max_dist = r - self.radius

        # ✅ Abpraller erst, wenn er wirklich draussen wäre
        if dist > max_dist and dist != 0:
            nx = dx / dist
            ny = dy / dist

            # zurück auf den Rand schieben
            self.x = cx + nx * max_dist
            self.y = cy + ny * max_dist

            # Geschwindigkeit spiegeln
            v_dot_n = self.vx * nx + self.vy * ny
            self.vx = self.vx - 2 * v_dot_n * nx
            self.vy = self.vy - 2 * v_dot_n * ny

        #Könnte hier noch abpraller einbauen, also das feuerball nicht einfach aus dem kreis herausfliegt

    def draw(self, screen):
        if not self.alive:
            return
        
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def kill(self):
        self.alive = False

# pygame.init()
# WIDTH = 500
# HEIGHT = 500
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# b1 = Feuerball(50, 50, 2, 5)
# b2 = Feuerball(100, 50, 5, 2)
# f = 0

# clock = pygame.time.Clock()

# running = True
# while running:

#     # WICHTIG: Event-Loop
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False


    # b1.update()
    # b2.update()

    # screen.fill("white")
    # b1.draw(screen)
    # b2.draw(screen)
    # pygame.display.flip()
    # clock.tick(60)

    # f = f + 1
#pygame.quit()