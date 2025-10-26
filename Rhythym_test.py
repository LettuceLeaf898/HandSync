import pygame
import time
import threading
import sys

# have a single light flashing the number of times for the rhythm 
# Initialize mixer and display
pygame.mixer.init()
pygame.init()

# Screen setup
WIDTH, HEIGHT = 400, 400 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beat Visualizer")

# Colors
BLACK = (10, 10, 10)
GRAY = (60, 60, 60)
KICK_COLOR = (255, 50, 50)
SNARE_COLOR = (50, 150, 255)
HIHAT_COLOR = (255, 255, 100)

# Circle Heights
kick_height = 80
snare_height = 320
hihat_height = 320
# Circle positions
kick_pos = (WIDTH // 2, kick_height)
snare_pos = (WIDTH // 2, snare_height)
hihat_pos = (WIDTH // 2, hihat_height)
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
count = 4
kick_pattern = 1
snare_pattern = 3

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
    if step%count ==kick_pattern:
        kick.play()
        kick_light = time.time()
    if step%count ==snare_pattern:
        snare.play()
        snare_light = time.time()
    if step>-1:
        hihat.play()
        hihat_light = time.time()

    # Draw background
    screen.fill(BLACK)

    # Draw circles — light up briefly
    now = time.time()
    pygame.draw.line(
        screen, (255, 255, 255), kick_pos, snare_pos, 5
    )

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
    # pygame.draw.circle(
    #     screen,
    #     HIHAT_COLOR if now - hihat_light < light_duration else GRAY,
    #     hihat_pos,
    #     radius,
    # )

    pygame.display.flip()
    time.sleep(beat_time)

    # Advance beat
    step = (step + 1) % 8
    clock.tick(60)

pygame.quit()
pygame.mixer.quit()
sys.exit()


