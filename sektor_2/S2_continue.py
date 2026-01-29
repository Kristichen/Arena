import random

def apply(sektor1_module):
    bälle = sektor1_module.get_bälle()
    alive = [b for b in bälle if b.alive]


    balls = sektor1_module.get_balls()
    alive = [b for b in balls if getattr(b, "alive", False)]

    if not alive:
        return

    random.shuffle(alive)
    kill_count = len(alive) // 2

    # Hälfte killen
    for b in alive[:kill_count]:
        b.kill()

    # Rest kleiner + langsamer
    for b in alive[kill_count:]:
        b.vx *= 0.5
        b.vy *= 0.5
        b.radius = max(2, int(b.radius / 2))

    sektor1_module.bleibendebälle_aktivieren()
    