import pygame
import random
import math

ARENA_RADIUS= 350
WIDTH, HEIGHT = 900, 900
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 350

pygame.init()
screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()

rauch_img = pygame.image.load("sektor 2/rauchball.png").convert_alpha()

def bleibt_in_arena(x, y, size):
    cx, cy = CENTER
    max_dist = ARENA_RADIUS - size // 2

    dx = x - cx
    dy = y - cy
    dist = math.hypot(dx, dy)

    if dist > max_dist:
        scale = max_dist / dist
        x = cx + dx * scale
        y = cy + dy * scale

    return x, y


class RauchWolke:
    def __init__(self, x, y):
        x, y = bleibt_in_arena(x, y, 30)
        self.layers = [(x, y, 30)]  # Startwolke (x, y, size)
        self.start_tick = pygame.time.get_ticks()
        self.spawn_index = 0

        times = [1.0]
        t = 3.0
        while t <= 20.0:
            times += [t, t + 1, t + 2]
            t += 5.0
        self.spawn_times_ms = [int(s * 1000) for s in times if s <= 20.0]

    def update(self):
        now = pygame.time.get_ticks() - self.start_tick
        while self.spawn_index < len(self.spawn_times_ms) and now >= self.spawn_times_ms[self.spawn_index]:
            self.spawn_one()
            self.spawn_index += 1

    def spawn_one(self):
        ax, ay, asize = random.choice(self.layers)

        new_size = random.randint(25, 40)  

        r_prev = asize / 2
        r_new = new_size / 2

        overlap = new_size / 5  

        distance = (r_prev + r_new) - overlap
        if distance < 2:
            distance = 2

        angle = random.uniform(0, 2 * math.pi)
        nx = ax + math.cos(angle) * distance
        ny = ay + math.sin(angle) * distance

        nx, ny = bleibt_in_arena(nx, ny, new_size)

        self.layers.append((nx, ny, new_size))

    def draw(self, surface):
        for x, y, size in self.layers:
            img = pygame.transform.scale(rauch_img, (size, size))  
            rect = img.get_rect(center=(int(x), int(y)))
            surface.blit(img, rect)

rauch_pos = [
    (425, 700),
    (350, 550),
    (200, 300),
    (550, 450),
    (500, 250),
    (700, 250),
    (250, 500),
    (675, 675)
]

rauch_zeiten = [0, 0, 3000, 6000, 9000, 12000, 14000, 16000]
rauchwolken = [None] * len(rauch_zeiten)
start_time = pygame.time.get_ticks()

rauch_zeiten = [0, 0, 3000, 6000, 9000, 12000, 14000, 16000]
rauchwolken = [None] * len(rauch_zeiten)
start_time = pygame.time.get_ticks()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = pygame.time.get_ticks() - start_time

    for i in range(len(rauchwolken)):
        if rauchwolken[i] is None and now >= rauch_zeiten[i]:
            x, y = rauch_pos[i]
            rauchwolken[i] = RauchWolke(x, y)

    screen.fill((240, 230, 200))
    pygame.draw.circle(screen, (120, 80, 40), CENTER, ARENA_RADIUS + 5)
    pygame.draw.circle(screen, (240, 240, 240), CENTER, ARENA_RADIUS)

    for r in rauchwolken:
        if r:
            r.update()
            r.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
