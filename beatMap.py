import pygame
import time
import threading
import sys

# Initialize mixer
pygame.mixer.init()

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

# Flag to stop the loop
running = True

# Function to listen for 'q' press in another thread
def listen_for_quit():
    global running
    while True:
        user_input = input()
        if user_input.lower() == 'q':
            running = False
            print("Stopping beat...")
            break

# Start listener thread
threading.Thread(target=listen_for_quit, daemon=True).start()

# Main beat loop
print("Playing beat... (press 'q' then Enter to stop)")
while running:
    for i in range(8):
        if not running:
            break
        if kick_pattern[i]:
            kick.play()
        if snare_pattern[i]:
            snare.play()
        if hihat_pattern[i]:
            hihat.play()
        time.sleep(beat_time)

pygame.mixer.quit()
sys.exit()
