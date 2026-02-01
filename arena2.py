import pygame
import math
import time

pygame.init()

WIDTH, HEIGHT = 900, 900
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 350

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spielarena mit Countdown und Sektoren")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)

SECTOR_COLORS = [
    (120, 220, 200),
    (40, 130, 120),
    (80, 110, 170),
    (20, 40, 90),
    (120, 200, 120),
    (40, 120, 60),
]

COUNTDOWN_TIME = 20
SECTOR_START_ANGLE = 270  # 12 Uhr (oben)

active_sector = 0
sector_running = True
sector_end_time = time.time() + COUNTDOWN_TIME


def draw_sector(screen, mitte, radius, winkel_start, winkel_ende, color):
    winkel_start %= 360
    winkel_ende %= 360

    points = [mitte]
    step = 2
    a = winkel_start

    while True:
        rad = math.radians(a)
        x = mitte[0] + radius * math.cos(rad)
        y = mitte[1] + radius * math.sin(rad)
        points.append((x, y))

        if a == winkel_ende:
            break

        a = (a - step) % 360  # gegen den Uhrzeigersinn

        ccw_dist_now = (a - winkel_ende) % 360
        ccw_dist_prev = ((a + step) - winkel_ende) % 360
        if ccw_dist_now > ccw_dist_prev:
            a = winkel_ende

    pygame.draw.polygon(screen, color, points)


def update_sector_effect(welcher_sektor, dt, events):
    pass


running = True
prev_time = time.time()

while running:
    now = time.time()
    dt = now - prev_time
    prev_time = now

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    time_left = int(sector_end_time - now)
    if time_left <= 0:
        active_sector = (active_sector + 1) % 6
        sector_end_time = now + COUNTDOWN_TIME
        sector_running = True
        time_left = COUNTDOWN_TIME

    screen.fill((240, 230, 200))
    pygame.draw.circle(screen, (120, 80, 40), CENTER, RADIUS + 5)
    pygame.draw.circle(screen, (240, 240, 240), CENTER, RADIUS)

    if sector_running:
        # CCW: 12->10->8->...
        start = SECTOR_START_ANGLE - active_sector * 60
        ende = start - 60
        draw_sector(screen, CENTER, RADIUS, start, ende, SECTOR_COLORS[active_sector])

        update_sector_effect(active_sector, dt, events)

    screen.blit(font.render(f"Countdown: {time_left}s", True, (0, 0, 0)), (WIDTH - 320, 30))
    screen.blit(font.render(f"Aktiver Sektor: {active_sector + 1}", True, (0, 0, 0)), (WIDTH -  320, 80))
    screen.blit(font.render(f"Sektor läuft: {sector_running}", True, (0, 0, 0)), (WIDTH - 320, 130))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()