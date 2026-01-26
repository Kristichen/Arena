import pygame
import math
import time

from constants import *
import sektoren.S1_Sektoraktivität as sektor1

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spielarena mit Countdown und Sektoren")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)

# Farben
SECTOR_COLORS = [
    (230, 220, 190 ),      # türkis hell [0]
    ( 40,130 ,120 ),    # türkis dunkel [1]
    (80 ,110 ,170 ),      # marine hell [2]
    (20 ,40 ,90 ),    # marine dunkel [3]
    (120, 200,120 ),    # grün hell [4]
    (40 ,120 ,60 ),    # grün dunkel [5]
]

COUNTDOWN_TIME = 20  
SEKTOR_START_WINKEL = 270
aktiver_sektor = 0  
sector_end_time = time.time() + COUNTDOWN_TIME
sektor1_war_aktiv = False


def sektort_von_position(pos):
    dx = pos[0] - CENTER[0]
    dy = pos [1] - CENTER[1]
    distance = math.sqrt(dx*dx + dy * dy)

    if distance >= ARENA_RADIUS:
        return None
    
    winkel = (math.degrees(math.atan2(dy,dx)) + 360) % 360
    return int(winkel // 60)

def draw_sector(screen, mitte, radius, winkel_start, winkel_ende, color):
    winkel_start %= 360
    winkel_ende %= 360
    
    points = [mitte]
    step = 2
    a = winkel_start

    while True:
        rad = math.radians(a) # von CHATGPT ERKLàRT
        x = mitte[0] + radius * math.cos(rad) # von CHATGPT ERKLàRT
        y = mitte[1] + radius * math.sin(rad) # von CHATGPT ERKLàRT
        points.append((x, y))
        
        if a == winkel_ende:
            break

        a = (a-step) % 360

        dist_now = (a - winkel_ende) % 360
        dist_previous = ((a+ step) - winkel_ende) % 360
        if dist_now > dist_previous:
            a = winkel_ende

    pygame.draw.polygon(screen, color, points)
    
def update_sector(welcher_sektor):
    global sektor1_war_aktiv

    sektor1_aktiv = (welcher_sektor == 0)

    if sektor1_aktiv and not sektor1_war_aktiv:
        sektor1.start(anzahl=20)

    if not sektor1_aktiv and sektor1_war_aktiv:
        sektor1.stop()

    if sektor1_aktiv:
        sektor1.update_and_draw(screen)

    sektor1_war_aktiv = sektor1_aktiv

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = time.time()

    time_left = int(sector_end_time - now)

    if time_left <= 0:
        aktiver_sektor = (aktiver_sektor + 1) % 6
        sector_end_time = now + COUNTDOWN_TIME
        time_left = COUNTDOWN_TIME

    screen.fill((240, 230, 200))
    pygame.draw.circle(screen, (120, 80, 40), CENTER, ARENA_RADIUS + 5)
    pygame.draw.circle(screen, (240, 240, 240), CENTER, ARENA_RADIUS)

    start = SEKTOR_START_WINKEL - aktiver_sektor * 60
    ende = start-60

    draw_sector(screen, CENTER, ARENA_RADIUS, start, ende, SECTOR_COLORS[aktiver_sektor])
    update_sector(aktiver_sektor)
    
    text_countdown = font.render(f"Countdown: {time_left}s", True, (0, 0, 0))
    screen.blit(text_countdown, (WIDTH - 300, 30))

    text_sector = font.render(f"Aktiver Sektor: {aktiver_sektor + 1}", True, (0, 0, 0))
    screen.blit(text_sector, (WIDTH - 320, 80))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
