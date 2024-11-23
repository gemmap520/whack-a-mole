import pygame
import random
import sys
from PIL import Image

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Whack-a-Fly")

fly_img = pygame.image.load("fly.png") #2
fly_img = pygame.transform.scale(fly_img, (60, 60))  #2
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

# log gif
raw_frames = load_gif_frames("stick-mozzerella.gif")
theface = [pygame.transform.scale(frame, (300, 200)) for frame in raw_frames]

current_frame = 0
frame_duration = 50
last_frame_time = pygame.time.get_ticks()

holes = [
    (175, 300),
    (375, 300),
    (575, 300),
    (175, 500),
    (375, 500),
    (575, 500)
]
######2
score = 0
fly_position = None
fly_visible = True
fly_appearance_time = random.randint(200, 300)
fly_duration = random.randint(200, 800)
fly_start_time = None
pygame.time.set_timer(pygame.USEREVENT, fly_appearance_time)
######

running = True
while running:
    screen.fill((255,255,255))
    now = pygame.time.get_ticks()
    if now - last_frame_time > frame_duration:
        current_frame = (current_frame + 1) % len(theface)
        last_frame_time = now
    frame_rect = theface[current_frame].get_rect(center=(screen_width // 2, screen_height // 2 - 150))
    screen.blit(theface[current_frame], frame_rect)
    for hole in holes:
        pygame.draw.circle(screen, (200, 200, 200), hole, 50)
    ##### 2
    if fly_visible and fly_position:
        fly_rect = fly_img.get_rect(center=fly_position)
        screen.blit(fly_img, fly_rect)
    #####
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        ###### 2
        elif event.type == pygame.USEREVENT:
            if not fly_visible:
                # Make the fly appear in a random hole
                fly_position = random.choice(holes)
                fly_visible = True
                # Set a timer to hide the fly after its duration
                pygame.time.set_timer(pygame.USEREVENT + 1, fly_duration)
            else:
                # Hide the fly and reset its appearance timer
                fly_visible = False
                fly_position = None
                pygame.time.set_timer(pygame.USEREVENT, fly_appearance_time)
        #######
    pygame.display.flip()
pygame.quit()
sys.exit()
