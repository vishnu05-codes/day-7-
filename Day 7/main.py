
import os
import sys
import math
import random
import pygame
import numpy as np

# ==========================================
# MAA DURGA - HIGH DETAIL PARTICLE ANIMATION
# ==========================================

pygame.init()

WIDTH = 720
HEIGHT = 960
FPS = 60

BACKGROUND = (5, 7, 18)
GOLD = (255, 190, 45)
BRIGHT_GOLD = (255, 225, 120)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maa Durga - Divine Particles")

clock = pygame.time.Clock()

title_font = pygame.font.SysFont("arial", 30, bold=True)
message_font = pygame.font.SysFont("arial", 24, bold=True)

# ==========================================
# LOAD IMAGE
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "durga.png")

if not os.path.isfile(IMAGE_PATH):
    print("ERROR: durga.png nahi mili!")
    print("Image ko main.py ke same folder mein rakho.")
    pygame.quit()
    sys.exit()

try:
    original_image = pygame.image.load(IMAGE_PATH).convert()
except pygame.error as error:
    print("Image loading error:", error)
    pygame.quit()
    sys.exit()

# Resize while preserving aspect ratio
source_width, source_height = original_image.get_size()

scale = min(
    (WIDTH - 30) / source_width,
    (HEIGHT - 120) / source_height
)

new_width = int(source_width * scale)
new_height = int(source_height * scale)

original_image = pygame.transform.smoothscale(
    original_image,
    (new_width, new_height)
)

image_x = (WIDTH - new_width) // 2
image_y = 65 + (HEIGHT - 120 - new_height) // 2

# ==========================================
# CREATE HIGH-DETAIL PARTICLES
# ==========================================

image_pixels = pygame.surfarray.array3d(original_image)

STEP = 2
points = []

for x in range(0, new_width, STEP):
    for y in range(0, new_height, STEP):

        r, g, b = image_pixels[x, y]

        points.append((
            image_x + x,
            image_y + y,
            (int(r), int(g), int(b))
        ))

random.shuffle(points)

particles = []

for target_x, target_y, color in points:

    angle = random.uniform(0, math.tau)
    distance = random.randint(100, 350)

    start_x = target_x + math.cos(angle) * distance
    start_y = target_y + math.sin(angle) * distance

    r, g, b = color
    brightness = (r + g + b) / 3

    if brightness > 180:
        radius = 2
    elif brightness > 80:
        radius = random.choice([1, 2])
    else:
        radius = 1

    particles.append({
        "x": start_x,
        "y": start_y,
        "target_x": target_x,
        "target_y": target_y,
        "color": color,
        "radius": radius
    })

print("Total particles:", len(particles))

# ==========================================
# GOLDEN BACKGROUND PARTICLES
# ==========================================

stars = []

for _ in range(150):
    stars.append({
        "x": random.randint(0, WIDTH - 1),
        "y": random.randint(0, HEIGHT - 1),
        "speed": random.uniform(0.3, 1.0),
        "radius": random.choice([1, 1, 2])
    })

# ==========================================
# ANIMATION SETTINGS
# ==========================================

frame = 0
DRAW_DURATION = 45 * FPS
running = True

# ==========================================
# MAIN ANIMATION LOOP
# ==========================================

while running:

    clock.tick(FPS)
    frame += 1

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_r:
                frame = 0

    screen.fill(BACKGROUND)

    # Moving background stars
    for star in stars:

        star["y"] += star["speed"]

        if star["y"] >= HEIGHT:
            star["y"] = 0
            star["x"] = random.randint(0, WIDTH - 1)

        pygame.draw.circle(
            screen,
            (100, 78, 40),
            (int(star["x"]), int(star["y"])),
            star["radius"]
        )

    # Reveal image progressively
    progress = min(frame / DRAW_DURATION, 1.0)
    visible_count = int(len(particles) * progress)

    for particle in particles[:visible_count]:

        particle["x"] += (
            particle["target_x"] - particle["x"]
        ) * 0.12

        particle["y"] += (
            particle["target_y"] - particle["y"]
        ) * 0.12

        pygame.draw.circle(
            screen,
            particle["color"],
            (
                int(particle["x"]),
                int(particle["y"])
            ),
            particle["radius"]
        )

    # Top heading
    title = title_font.render(
        "JAI MATA DI",
        True,
        GOLD
    )

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 20)
    )

    # Final message
    if progress >= 1.0:

        message = message_font.render(
            "SHUBH NAVRATRI",
            True,
            BRIGHT_GOLD
        )

        screen.blit(
            message,
            (
                WIDTH // 2 - message.get_width() // 2,
                HEIGHT - 40
            )
        )

    pygame.display.flip()

pygame.quit()
sys.exit()

