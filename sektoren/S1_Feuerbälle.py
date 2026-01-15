import pygame

class Feuerball:
    def __init__(self, x, y, vx, vy):
        self.x = float(x)
        self.y = float(y)
        self.vy = float(vy)
        self.vx = float(vx)
        self.radius = 15
        self.alive = True
        self.color = "red"       

    def update(self):
        if not self.alive:
            return 
        
        self.x += self.vx
        self.y += self.vy

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