import pygame
import math
import os
import random

pygame.init()

# ------------------------------------------------------------
# Arena-Setup (Test)
# ------------------------------------------------------------
WIDTH, HEIGHT = 900, 900
CENTER = (WIDTH // 2, HEIGHT // 2)
ARENA_RADIUS = 330

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Erdriss-Test (verzweigt wie grün)")
clock = pygame.time.Clock()

# ------------------------------------------------------------
# Bilder laden + NORMALISIEREN
# ------------------------------------------------------------
base = os.path.dirname(__file__)
img1_raw = pygame.image.load(os.path.join(base, "risse1.png")).convert_alpha()
img2_raw = pygame.image.load(os.path.join(base, "risse2.png")).convert_alpha()

# Wichtig: Bei sehr extremen PNGs ist es oft besser, auf "LÄNGE" zu skalieren.
# Wir nehmen dafür die grössere Bilddimension als Referenz (damit 10000 nicht killt).
TARGET_MAX_DIM = 120  # <- wie lang ein Riss-Segment ungefähr sein soll (in Spielpixeln)

w0, h0 = img1_raw.get_size()
base_scale = TARGET_MAX_DIM / max(w0, h0)

def scale_to_base(img):
    w, h = img.get_size()
    nw = max(1, int(w * base_scale))
    nh = max(1, int(h * base_scale))
    return pygame.transform.smoothscale(img, (nw, nh))

riss1_img = scale_to_base(img1_raw)
riss2_img = scale_to_base(img2_raw)

print("Original:", (w0, h0), "-> Base:", riss1_img.get_size(), "scale:", base_scale)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def punkte_auf_Kreisbogen(cx, cy, r, deg_start, deg_end, step_deg=1):
    pts = []
    deg_start %= 360
    deg_end %= 360
    if deg_start <= deg_end:
        degrees = range(deg_start, deg_end + 1, step_deg)
    else:
        degrees = list(range(deg_start, 360, step_deg)) + list(range(0, deg_end + 1, step_deg))
    for d in degrees:
        w = math.radians(d)
        pts.append((cx + r * math.cos(w), cy + r * math.sin(w)))
    return pts

def bleibt_in_arena(x, y, margin=0):
    cx, cy = CENTER
    max_dist = ARENA_RADIUS - margin
    dx = x - cx
    dy = y - cy
    dist = math.hypot(dx, dy)
    if dist > max_dist and dist != 0:
        s = max_dist / dist
        x = cx + dx * s
        y = cy + dy * s
    return x, y

def unit(dx, dy):
    d = math.hypot(dx, dy)
    if d == 0:
        return 1.0, 0.0
    return dx / d, dy / d


# ------------------------------------------------------------
# RissSegment: wächst "von einem Punkt" (Root) ins Feld
# ------------------------------------------------------------
class RissSegment:
    """
    Root = Punkt, wo der Riss startet / andockt.
    Wir zeichnen das Bild so, dass es vom Root aus in Richtung angle "rauszeigt".
    """
    def __init__(self, root_x, root_y, angle, scale=1.0, image=riss1_img):
        self.root_x = float(root_x)
        self.root_y = float(root_y)
        self.angle = float(angle)       # rad
        self.scale = float(scale)       # 0.7..1.2 usw.
        self.image = image

        # Lebensdauer, damit es nicht unendlich voll wird (kannst du erhöhen)
        self.life = random.uniform(4.5, 7.5)
        self.age = 0.0
        self.alive = True

    def update(self, dt):
        self.age += dt
        if self.age >= self.life:
            self.alive = False

    def switch_image(self):
        self.image = riss2_img

    def get_end_point(self):
        """
        Gibt den 'Endpunkt' des Segmentes zurück (ungefähr),
        damit Kinder dort oder nahe dran spawnen können.
        """
        # Wir schätzen die Länge über die Bildhöhe (nach Transformation)
        img = pygame.transform.rotozoom(self.image, -math.degrees(self.angle), self.scale)
        length = img.get_height() * 0.55  # Faktor -> fühlt sich natürlicher an

        ex = self.root_x + math.cos(self.angle) * length
        ey = self.root_y + math.sin(self.angle) * length
        return ex, ey

    def draw(self, surface):
        # Transformieren
        img = pygame.transform.rotozoom(self.image, -math.degrees(self.angle), self.scale)

        # Trick: Wir wollen, dass der Root-Punkt NICHT in der Bildmitte ist,
        # sondern eher am "hinteren" Ende des Dreiecks.
        # Annahme: Dreieck zeigt im Bild nach "oben" (Spitze oben).
        # Dann ist Root nahe unten in der Mitte.
        root_in_img = (img.get_width() // 2, int(img.get_height() * 0.80))

        # Damit root_in_img auf (root_x, root_y) landet:
        draw_x = int(self.root_x - root_in_img[0])
        draw_y = int(self.root_y - root_in_img[1])

        surface.blit(img, (draw_x, draw_y))


# ------------------------------------------------------------
# RissSystem: verzweigt wie grün
# ------------------------------------------------------------
class RissSystem:
    def __init__(self):
        self.segments = []
        self.timer = 0.0
        self.spawn_interval = 3.0

        # Start: ein Root auf Kreisbogen 330° -> 30°
        arc = punkte_auf_Kreisbogen(CENTER[0], CENTER[1], ARENA_RADIUS, 330, 30, 1)
        x, y = random.choice(arc)

        # Richtung ins Zentrum (plus starke Streuung -> organischer)
        dx = CENTER[0] - x
        dy = CENTER[1] - y
        ux, uy = unit(dx, dy)
        base_angle = math.atan2(uy, ux) + random.uniform(-0.6, 0.6)

        # etwas nach innen drücken
        x += ux * 18
        y += uy * 18
        x, y = bleibt_in_arena(x, y, margin=10)

        self.segments.append(
            RissSegment(x, y, base_angle, scale=random.uniform(0.95, 1.15), image=riss1_img)
        )

    def spawn_branch(self):
        """
        Alle 3 Sekunden:
        - wähle 1-2 bestehende Segmente
        - an deren Root oder nahe beim Endpunkt spawne 2-4 neue Äste
        - danach: alle bisherigen wechseln auf Bild2
        """
        if not self.segments:
            return

        parents = random.sample(self.segments, k=min(len(self.segments), random.randint(1, 2)))

        for p in parents:
            # Spawnpunkt: entweder am Root oder nahe am Endpunkt
            if random.random() < 0.45:
                sx, sy = p.root_x, p.root_y
            else:
                ex, ey = p.get_end_point()
                # bisschen Jitter, damit es "kritzeliger" wirkt
                sx = ex + random.uniform(-12, 12)
                sy = ey + random.uniform(-12, 12)

            # in Arena halten
            sx, sy = bleibt_in_arena(sx, sy, margin=12)

            # 2-4 neue Äste in verschiedenen Richtungen (grün-like)
            n_children = random.randint(2, 4)
            for _ in range(n_children):
                # starke Richtungsvariation um den Elternwinkel
                a = p.angle + random.uniform(-1.4, 1.4)

                # eher kürzer/kleiner, damit es wie Äste aussieht
                sc = p.scale * random.uniform(0.65, 0.95)

                # Root leicht auseinanderziehen (damit nicht alles exakt gleich startet)
                ox = sx + random.uniform(-10, 10)
                oy = sy + random.uniform(-10, 10)
                ox, oy = bleibt_in_arena(ox, oy, margin=12)

                self.segments.append(RissSegment(ox, oy, a, scale=sc, image=riss1_img))

        # alle bisherigen -> Bild 2 (wie du wolltest)
        for s in self.segments:
            s.switch_image()

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.spawn_interval:
            self.timer -= self.spawn_interval
            self.spawn_branch()

        for s in self.segments:
            s.update(dt)
        self.segments = [s for s in self.segments if s.alive]

    def draw(self, surface):
        for s in self.segments:
            s.draw(surface)


# ------------------------------------------------------------
# Main Loop
# ------------------------------------------------------------
risse = RissSystem()
running = True

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    risse.update(dt)

    # Arena zeichnen (wie du wolltest)
    screen.fill((240, 230, 200))
    pygame.draw.circle(screen, (120, 80, 40), CENTER, ARENA_RADIUS + 5)
    pygame.draw.circle(screen, (240, 240, 240), CENTER, ARENA_RADIUS)

    risse.draw(screen)

    pygame.display.flip()

pygame.quit()

