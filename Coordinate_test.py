import pygame
import time
import threading
import sys

# Initialize mixer and display
pygame.mixer.init()
pygame.init()

# Screen setup
WIDTH, HEIGHT = 405, 425 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beat Visualizer")

# Colors
BLACK = (10, 10, 10)
GRAY = (60, 60, 60)
LEFT_COLOR = (255, 50, 50)
RIGHT_COLOR = (50, 150, 255)

#Margins
radius = 40
top_margin = 80
left_margin = 50

# Light-up timers
circle1_light = 0
circle2_light = 0
circle3_light = 0
light_duration = 0.15  # seconds

# Load sounds
kick = pygame.mixer.Sound("sounds/KICK.wav")
snare = pygame.mixer.Sound("sounds/SNARE.wav")
hihat = pygame.mixer.Sound("sounds/HIHAT.wav")

# Beat patterns (8 steps)

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

def one_circle(hand):
    now = time.time()
    #create a circle
    if hand == "left":
        circle1_pos = (left_margin, top_margin)
        color = LEFT_COLOR
    else:
        circle1_pos = (WIDTH//2 +left_margin, top_margin)
        color = RIGHT_COLOR
    
    pygame.draw.circle(
        screen,
        color,
        circle1_pos,
        radius,
    )

def two_circle(hand, step):
    now = time.time()
    if hand == "left":
        circle1_pos = (left_margin, top_margin)
        color = LEFT_COLOR
        circle2_pos = (left_margin, HEIGHT-top_margin)
    else:
        circle1_pos = (WIDTH//2 +left_margin, top_margin)
        color = RIGHT_COLOR
        circle2_pos = (WIDTH//2 +left_margin, HEIGHT-top_margin)
    #set up timers
    circle1_light = 0
    circle2_light = 0
    
    if(step ==0): circle1_light = time.time()
    if(step ==1): circle2_light = time.time()

    # draw circles and lines
    pygame.draw.line(
        screen, (255, 255, 255),  circle1_pos, circle2_pos, 5
    )

    pygame.draw.circle(
        screen,
        color if now - circle1_light < light_duration else GRAY,
        circle1_pos,
        radius,
    )
    
    pygame.draw.circle(
        screen,
        color if now - circle2_light < light_duration else GRAY,
        circle2_pos,
        radius,
    )
def three_circle(hand, step):
    now = time.time()
    if hand == "left":
        color = LEFT_COLOR
        circle1_pos = (left_margin, top_margin)
        circle2_pos = (left_margin, HEIGHT-top_margin)
        circle3_pos = (left_margin+100, HEIGHT-top_margin)

    else:
        color = RIGHT_COLOR
        circle1_pos = (WIDTH//2 +left_margin, top_margin)
        circle2_pos = (WIDTH//2 +left_margin, HEIGHT-top_margin)
        circle3_pos = (WIDTH//2 +left_margin+100, HEIGHT-top_margin)
    
    #set up lights
    circle1_light = 0
    circle2_light = 0
    circle3_light = 0
    if(step ==0): circle1_light = time.time()
    if(step ==1): circle2_light = time.time()
    if(step ==2): circle3_light = time.time()

    #draw circles and lines
    pygame.draw.line(
        screen, (255, 255, 255),  circle1_pos, circle2_pos, 5
    )
    pygame.draw.line(
        screen, (255, 255, 255),  circle2_pos, circle3_pos, 5
    )
    pygame.draw.line(
        screen, (255, 255, 255),  circle3_pos, circle1_pos, 5
    )

    pygame.draw.circle(
        screen,
        color if now - circle1_light < light_duration else GRAY,
        circle1_pos,
        radius,
    )
    
    pygame.draw.circle(
        screen,
        color if now - circle2_light < light_duration else GRAY,
        circle2_pos,
        radius,
    )
    pygame.draw.circle(
        screen,
        color if now - circle3_light< light_duration else GRAY,
        circle3_pos,
        radius,
    )


left_beat = 2
right_beat = 3
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw background
    screen.fill(BLACK)

    # Draw circles — light up briefly
    if(left_beat == 1):
        one_circle("left")
    elif(left_beat == 2):
        two_circle("left", step%2)
    elif(left_beat == 3):
        three_circle("left", step%3)
    else:
        print("error")

    if(right_beat == 1):
        one_circle("right")
    elif(right_beat == 2):
        two_circle("right", step%2)
    elif(right_beat == 3):
        three_circle("right", step%3)
    else:
        print("error")  

    pygame.display.flip()
    time.sleep(beat_time)

    # Advance beat
    step = (step + 1)%6
    clock.tick(60)

pygame.quit()
pygame.mixer.quit()
sys.exit()


