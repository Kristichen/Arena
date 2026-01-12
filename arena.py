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

# Farben
SECTOR_COLORS = [
    (120 ,220 ,200 ),      # türkis hell [0]
    ( 40,130 ,120 ),    # türkis dunkel [1]
    (80 ,110 ,170 ),      # marine hell [2]
    (20 ,40 ,90 ),    # marine dunkel [3]
    (120, 200,120 ),    # grün hell [4]
    (40 ,120 ,60 ),    # grün dunkel [5]
]

current_sector = 0  
sector_aktiv = [False, False, False, False, False, False]

COUNTDOWN_TIME = 20  
sector_end_time = time.time() + COUNTDOWN_TIME

def sektort_von_position(pos):
    dx = pos[0] - CENTER[0]
    dy = pos [1] - CENTER[1]
    distance = math.sqrt(dx*dx + dy * dy)

    if distance >= RADIUS:
        return None
    
    winkel = (math.degrees(math.atan2(dy,dx)) + 360) % 360
    return int(winkel // 60)

def draw_sector(screen, mitte, radius, winkel_start, winkel_ende, color):
    points = [mitte]
    step = 2
    for angle in range(winkel_start, winkel_ende + 1, step):
        rad = math.radians(angle) # von CHATGPT ERKLàRT
        x = mitte[0] + radius * math.cos(rad) # von CHATGPT ERKLàRT
        y = mitte[1] + radius * math.sin(rad) # von CHATGPT ERKLàRT
        points.append((x, y))
    pygame.draw.polygon(screen, color, points)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    time_left = int(sector_end_time - time.time())

    if time_left <= 0:
        current_sector = (current_sector + 1) % 6
        sector_end_time = time.time() + COUNTDOWN_TIME
        time_left = COUNTDOWN_TIME

    screen.fill((240, 230, 200))

    pygame.draw.circle(screen, (120, 80, 40), CENTER, RADIUS + 5)
    pygame.draw.circle(screen, (240, 240, 240), CENTER, RADIUS)

    # Aktiven Sektor färben
    start = current_sector * 60
    ende = start + 60
    draw_sector(screen, CENTER, RADIUS, start, ende, SECTOR_COLORS[current_sector])


    text_countdown = font.render(f"Countdown: {time_left}s", True, (0, 0, 0))
    screen.blit(text_countdown, (WIDTH - 300, 30))

    text_sector = font.render(f"Aktiver Sektor: {current_sector + 1}", True, (0, 0, 0))
    screen.blit(text_sector, (WIDTH - 320, 80))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
