import pygame
import time
import threading
import sys

# Initialize mixer and display
pygame.mixer.init()
pygame.init()

# Screen setup
WIDTH, HEIGHT = 400, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beat Visualizer")

# Colors
BLACK = (10, 10, 10)
GRAY = (60, 60, 60)
KICK_COLOR = (255, 50, 50)
SNARE_COLOR = (50, 150, 255)
HIHAT_COLOR = (255, 255, 100)

# Circle positions
kick_pos = (80, HEIGHT // 2)
snare_pos = (200, HEIGHT // 2)
hihat_pos = (320, HEIGHT // 2)
radius = 40

# Light-up timers
kick_light = 0
snare_light = 0
hihat_light = 0
light_duration = 0.15  # seconds

# Load sounds
kick = pygame.mixer.Sound("sounds/KICK.wav")
snare = pygame.mixer.Sound("sounds/SNARE.wav")
hihat = pygame.mixer.Sound("sounds/HIHAT.wav")

# Beat patterns (8 steps)
kick_pattern = [1, 0, 0, 0, 1, 0, 0, 0]
snare_pattern = [0, 0, 1, 0, 0, 0, 1, 0]
hihat_pattern = [1, 1, 1, 1, 1, 1, 1, 1]

# Tempo (BPM)
bpm = 120
beat_time = 60 / bpm

running = True

# Thread for 'q' input
def listen_for_quit():
    global running
    while True:
        user_input = input()
        if user_input.lower() == 'q':
            running = False
            print("Stopping beat...")
            break

threading.Thread(target=listen_for_quit, daemon=True).start()

# Main beat loop
print("Playing beat... (press 'q' then Enter to stop)")
clock = pygame.time.Clock()

step = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Beat step trigger
    if kick_pattern[step]:
        kick.play()
        kick_light = time.time()
    if snare_pattern[step]:
        snare.play()
        snare_light = time.time()
    if hihat_pattern[step]:
        hihat.play()
        hihat_light = time.time()

    # Draw background
    screen.fill(BLACK)

    # Draw circles — light up briefly
    now = time.time()
    pygame.draw.circle(
        screen,
        KICK_COLOR if now - kick_light < light_duration else GRAY,
        kick_pos,
        radius,
    )
    pygame.draw.circle(
        screen,
        SNARE_COLOR if now - snare_light < light_duration else GRAY,
        snare_pos,
        radius,
    )
    pygame.draw.circle(
        screen,
        HIHAT_COLOR if now - hihat_light < light_duration else GRAY,
        hihat_pos,
        radius,
    )

    pygame.display.flip()
    time.sleep(beat_time)

    # Advance beat
    step = (step + 1) % 8
    clock.tick(60)

pygame.quit()
pygame.mixer.quit()
sys.exit()


