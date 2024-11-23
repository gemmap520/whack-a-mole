import pygame
import random
import sys
from PIL import Image

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("no no no no no no no no no no.py")

def load_gif_frames(gif_path):
    gif = Image.open(gif_path)
    frames = []
    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_surface = pygame.image.fromstring(
            gif.convert("RGBA").tobytes(), gif.size, "RGBA"
        )
        frames.append(frame_surface)
    return frames

raw_frames = load_gif_frames("stick-mozzerella.gif")
theface = [pygame.transform.scale(frame, (300, 200)) for frame in raw_frames]

current_frame = 0
frame_duration = 50
last_frame_time = pygame.time.get_ticks()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    now = pygame.time.get_ticks()
    if now - last_frame_time > frame_duration:
        current_frame = (current_frame + 1) % len(theface)
        last_frame_time = now

    screen.fill((255,255,255))
    frame_rect = theface[current_frame].get_rect(center=(screen_width // 2, screen_height // 2 - 150))
    screen.blit(theface[current_frame], frame_rect)
    pygame.display.flip()
pygame.quit()
sys.exit()
