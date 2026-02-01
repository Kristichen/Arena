import pygame
import math
import time

from constants import *
from player import Player
import sektor0.S1_Sektoraktivität as feuer
import sektor0.S1_Sektordeaktivieren as feuerloescher
import sektor2.S2_Sektoraktivität as rauch
import sektor5.S5_Sektoraktivität as wasser 

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spielarena mit Countdown und Sektoren")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)
rauch.init_images()
wasser.init_images()
feuerloescher.init_images()

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
player = Player(WIDTH//2, HEIGHT//2 + 120, vx=4, vy=4)

feuer_war_aktiv = False
laser_war_aktiv = False
rauch_war_aktiv = False
wasser_war_aktiv = False

sektor1_erloest = False 

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
    global feuer_war_aktiv, laser_war_aktiv, rauch_war_aktiv, wasser_war_aktiv

    feuer_aktiv = (welcher_sektor == 0)
    laser_aktiv = (welcher_sektor == 1)
    rauch_aktiv = (welcher_sektor == 2)
    wasser_aktiv = (welcher_sektor == 5)

# FEUER
    if feuer_aktiv and not feuer_war_aktiv:
        feuer.start(anzahl=20)
        feuerloescher.reset()

    if not feuer_aktiv and feuer_war_aktiv:
        feuerloescher.aktiv_machen(False)
        
    if feuer_aktiv:
        feuer.update_and_draw(screen)
# RAUCH
    if rauch_aktiv and not rauch_war_aktiv:
        rauch.start()
    if not rauch_aktiv and rauch_war_aktiv:
        rauch.stop()
    if rauch_aktiv:
        rauch.update_and_draw(screen)

# WASSER
    if wasser_aktiv and not wasser_war_aktiv:
        wasser.start()
    if not wasser_aktiv and wasser_war_aktiv:
        wasser.stop()
    if wasser_aktiv:
        wasser.update_and_draw(screen)


    feuer_war_aktiv = feuer_aktiv
    laser_war_aktiv = laser_aktiv
    rauch_war_aktiv = rauch_aktiv
    wasser_war_aktiv = wasser_aktiv

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = time.time()

    time_left = int(sector_end_time - now)

    if time_left <= 0:        
        if aktiver_sektor == 0:
            feuerloescher.aktiv_machen(False)

        aktiver_sektor = (aktiver_sektor + 1) % 6
        sector_end_time = now + COUNTDOWN_TIME
        time_left = COUNTDOWN_TIME

    pressed = pygame.key.get_pressed()
    player.update(pressed)

    screen.fill((240, 230, 200))
    pygame.draw.circle(screen, (120, 80, 40), CENTER, ARENA_RADIUS + 5)
    pygame.draw.circle(screen, (240, 240, 240), CENTER, ARENA_RADIUS)

    start = SEKTOR_START_WINKEL - aktiver_sektor * 60
    ende = start-60

    draw_sector(screen, CENTER, ARENA_RADIUS, start, ende, SECTOR_COLORS[aktiver_sektor])
    feuerloescher.draw(screen)
    update_sector(aktiver_sektor)

    if aktiver_sektor == 0:
        feuerloescher.check_and_deactivate(player, feuer)

        if player.alive and feuer.player_hit(player):
            player.alive = False
            feuer.stop()

    if aktiver_sektor == 2:
        if player.alive and rauch.player_hit(player):
            player.alive = False
            rauch.stop()

    if aktiver_sektor == 5:
        if player.alive and wasser.player_hit(player):
            player.alive = False
            wasser.stop()

    player.draw(screen)

    text_countdown = font.render(f"Countdown: {time_left}s", True, (0, 0, 0))
    screen.blit(text_countdown, (WIDTH - 300, 30))

    text_sector = font.render(f"Aktiver Sektor: {aktiver_sektor + 1}", True, (0, 0, 0))
    screen.blit(text_sector, (WIDTH - 320, 80))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
