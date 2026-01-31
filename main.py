import pygame
import math
import time

from constants import *
from laser import Laser
from player import Player
import sektoren.S1_Sektoraktivität as sektor1
import sektoren.S1_Sektordeaktivieren as erloesen

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
arena=pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Fate of Nature: Survive the Arena")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)

# Farben
SECTOR_COLORS = [
    (120 ,220 ,200 ),      # türkis hell [0]
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
sektor2_war_aktiv = False
letzter_sektor = aktiver_sektor


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
        #sektor1.stop()  
        sektor1.start(anzahl=20)

    if not sektor1_aktiv and sektor1_war_aktiv:
        sektor1.stop()

    if sektor1_aktiv:
        sektor1.update_and_draw(arena)


    #if sektor1.is_bleibende():
    #    sektor1.update_and_draw(screen)

    sektor1_war_aktiv = sektor1_aktiv



def update_laser(welcher_sektor):
    global sektor2_war_aktiv

    laser_aktiv = (welcher_sektor == 1)

    if laser_aktiv and not sektor2_war_aktiv:
        laser.start()

    if not laser_aktiv and sektor2_war_aktiv:
        laser.stop()

    sektor2_war_aktiv = laser_aktiv



running = True
player = Player(WIDTH//2, HEIGHT//2 + 120, vx=4, vy=4)
laser=Laser(start_sector=1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = time.time()
    time_left = int(sector_end_time - now)

    if time_left <= 0:
        letzter_sektor = aktiver_sektor

        if aktiver_sektor == 0:
            sektor1_erloest = False 

        aktiver_sektor = (aktiver_sektor + 1) % 6
        sector_end_time = now + COUNTDOWN_TIME
        time_left = COUNTDOWN_TIME

    pressed = pygame.key.get_pressed()
    player.update(pressed)
    update_laser(aktiver_sektor)
    laser.update()

    screen.fill((240, 230, 200))

    pygame.draw.circle(arena, (120, 80, 40), CENTER, RADIUS + 5)
    pygame.draw.circle(arena, (240, 240, 240), CENTER, RADIUS)

        # Aktiven Sektor färben
    start = SEKTOR_START_WINKEL - aktiver_sektor * 60
    ende = start-60

    draw_sector(arena, CENTER, RADIUS, start, ende, SECTOR_COLORS[aktiver_sektor])
    erloesen.draw(arena)
    update_sector(aktiver_sektor)

    if aktiver_sektor == 0:
        erloesen.check_and_deactivate(player, sektor1)

        if player.alive and sektor1.player_hit(player):
            player.alive = False
            sektor1.stop()

    if laser.is_on and not laser.turned_off:
        if laser.player_hit(player) and player.on_ground:
            player.alive = False
            laser.stop()

        if laser.jumped_over(player) and laser.player_hit(player):
            laser.stop()
    laser.draw(arena)

    text_countdown = font.render(f"Countdown: {time_left}s", True, (0, 0, 0))
    screen.blit(text_countdown, (WIDTH - 300, 30))

    text_sector = font.render(f"Aktiver Sektor: {aktiver_sektor + 1}", True, (0, 0, 0))
    screen.blit(text_sector, (WIDTH - 320, 80))
    

    zoom = player.get_zoom()
    scaled_w = int(WIDTH * zoom)
    scaled_h = int(HEIGHT * zoom)
    scaled_arena = pygame.transform.smoothscale(arena, (scaled_w, scaled_h))

    arena_x = (WIDTH - scaled_w) // 2
    arena_y = (HEIGHT - scaled_h) // 2

    screen.blit(scaled_arena, (arena_x, arena_y)) 

    player.draw(screen)

    pygame.display.flip()

    clock.tick(60)  

pygame.quit()