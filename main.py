import pygame
import math
import time

from constants import *
from player import Player
from laser import Laser
from bomb import Bomb
import sektor0.S1_Sektoraktivität as feuer
import sektor0.S1_Sektordeaktivieren as feuerlöscher
import sektor2.S2_Sektoraktivität as rauch
import sektor5.S5_Sektoraktivität as wasser 

#print("Rauch-Modul:", rauch.__file__)
#print("Hat init_images?", hasattr(rauch, "init_images"))

#print("Wasser-Modul:", wasser.__file__)
#print("Hat init_images?", hasattr(wasser, "init_images"))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
arena=pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Spielarena mit Countdown und Sektoren")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)
rauch.init_images()
wasser.init_images()
feuerlöscher.init_images()
laser=Laser(start_sector=1)
# After pygame.init() and before main loop
try:
    arena_floor_img = pygame.image.load("Bilder/arena.png").convert_alpha()
    # Scale to fit the arena size
    floor_size = ARENA_RADIUS * 2
    arena_floor_img = pygame.transform.scale(arena_floor_img, (floor_size, floor_size))
    print("Arena floor image loaded successfully")
except:
    print("Could not load arena.png. Using default white circle.")
    arena_floor_img = None  # We'll fall back to white circle

# Farben
SECTOR_COLORS = [
    (230, 220, 190 ),      # türkis hell [0]
    ( 40,130 ,120 ),    # türkis dunkel [1]
    (80 ,110 ,170 ),      # marine hell [2]
    (20 ,40 ,90 ),    # marine dunkel [3]
    (120, 200,120 ),    # grün hell [4]
    (40 ,120 ,60 ),    # grün dunkel [5]
]
GAME_START=-1
GAME_RUNNING = 0
GAME_OVER   = 1
GAME_WIN    = 2

sektor_comlited=0
game_state = GAME_START

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

#if aktiver_sektor == 0:
#    if erloesen.check_and_deactivate(player, sektor1):
#        sektor1_erloest = True

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
    if not feuer_aktiv and feuer_war_aktiv:
        feuer.stop()
    if feuer_aktiv:
        feuer.update_and_draw(arena)
#LASER
    if laser_aktiv and not laser_war_aktiv:
        laser.start()
    if not laser_aktiv and laser_war_aktiv:
        laser.stop()
    if laser_aktiv:
        laser.update()
        laser.draw(arena)
# RAUCH
    if rauch_aktiv and not rauch_war_aktiv:
        rauch.start()
    if not rauch_aktiv and rauch_war_aktiv:
        rauch.stop()
    if rauch_aktiv:
        rauch.update_and_draw(arena)

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

bombs=[]
last_bomb= pygame.time.get_ticks()
interval=500
bomb_active=False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == GAME_START:
                game_state = GAME_RUNNING
                start_time = time.time()
            elif event.key == pygame.K_ESCAPE and game_state != GAME_RUNNING:
                running = False
    if game_state == GAME_START:
        screen.fill((0, 0, 0))
        text_start = font .render ("Press any key to start", True, (255, 255, 255))
        screen.blit (text_start, (WIDTH // 2 - text_start.get_width() // 2, HEIGHT // 2 - text_start.get_height() // 2))
        pygame.display.flip()
        continue
    now = time.time()
    time_left = int(sector_end_time - now)

    if time_left <= 0 and game_state == GAME_RUNNING:   
        aktiver_sektor = (aktiver_sektor + 1) % 6   
        sector_end_time = now + COUNTDOWN_TIME
        time_left = COUNTDOWN_TIME  

        if aktiver_sektor == 0:
            sektor1_erloest = False 
            sektor_comlited+=1
        if sektor_comlited >=1:
            game_state = GAME_WIN

    pressed = pygame.key.get_pressed()
    player.update(pressed)

    start = SEKTOR_START_WINKEL - aktiver_sektor * 60
    ende = start-60
    screen.fill((240, 230, 200))
    pygame.draw.circle(arena, (120, 80, 40), CENTER, ARENA_RADIUS + 5)
    draw_sector(arena, CENTER, ARENA_RADIUS+5, start, ende, SECTOR_COLORS[aktiver_sektor])
    if arena_floor_img is not None:
    # Draw the arena image
        arena.blit(arena_floor_img, arena_floor_img.get_rect(center=CENTER))
    else:
    # Fallback: draw white circle if image not found
        pygame.draw.circle(arena, (240, 240, 240), CENTER, ARENA_RADIUS)


    
    feuerlöscher.draw(arena)
    update_sector(aktiver_sektor)

    if player.alive == False:
        game_state = GAME_OVER
    if game_state == GAME_RUNNING:
        if aktiver_sektor == 0:
            feuerlöscher.check_and_deactivate(player, feuer)

        if player.alive and feuer.player_hit(player):
            player.alive = False
            feuer.stop()

        if aktiver_sektor == 2:
            if player.alive and rauch.player_hit(player):
                player.alive = False
                rauch.stop()

        now_ticks = pygame.time.get_ticks()
        if aktiver_sektor == 3:
            if not bomb_active:
                bomb_active=True
                last_bomb=now_ticks
        else:
            if bomb_active:
                bomb_active=False
            

        if aktiver_sektor == 5:
            if player.alive and wasser.player_hit(player):
                player.alive = False
                wasser.stop()

        if laser.is_on and not laser.turned_off:
            if laser.player_hit(player) and player.on_ground:
                player.alive = False
                laser.stop()

        if laser.jumped_over(player) and laser.player_hit(player):
            laser.stop()
        laser.draw(arena)

        if bomb_active and aktiver_sektor==3:
            if now_ticks - last_bomb > interval:
                bombs.append(Bomb())
                last_bomb = now_ticks
        if pressed[pygame.K_w]:
            for b in bombs[:]: 
                if b.defuse(player):
                    bombs.remove(b)
        for b in bombs[:]:
            b.update()
            b.draw(arena)
            if b.player_hit(player):
                player.alive = False
            if b.exploded:
                if now_ticks >= b.expl_end:
                    bombs.remove(b)

    
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
    if game_state != GAME_RUNNING:
        end_screen = pygame.Surface((WIDTH, HEIGHT))
        end_screen.fill((0, 0, 0,180))
        screen.blit(end_screen, (0, 0))

        if game_state == GAME_OVER:
            text_game_over = font.render("Game Over!", True, (255, 0, 0))
            screen.blit(text_game_over, (WIDTH // 2 - text_game_over.get_width() // 2, HEIGHT // 2 - text_game_over.get_height() // 2))
        elif game_state == GAME_WIN:
            text_game_win = font.render("You Win!", True, (0, 255, 0))
            screen.blit(text_game_win, (WIDTH // 2 - text_game_win.get_width() // 2, HEIGHT // 2 - text_game_win.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()