import pygame
import random
import sys
from PIL import Image

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Whack-a-Fly")

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
fly_img = pygame.image.load("fly.png")
fly_img = pygame.transform.scale(fly_img, (60, 60))
current_frame = 0
frame_duration = 50
last_frame_time = pygame.time.get_ticks()

umbrella_img = pygame.image.load("umbrella.png")
umbrella_img = pygame.transform.scale(umbrella_img, (100, 100))

holes = [
    (175, 300),
    (375, 300),
    (575, 300),
    (175, 500),
    (375, 500),
    (575, 500)
]
score = 0
fly_position = None
fly_visible = True
fly_appearance_time = random.randint(500, 1000)
fly_duration = random.randint(1000, 2000)
fly_start_time = None
game_time_limit = 30000  # 6
start_time = pygame.time.get_ticks() # 6
pygame.time.set_timer(pygame.USEREVENT, fly_appearance_time)
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)
running = True
while running:
    screen.fill((255,255,255))
##### 6
    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time >= game_time_limit:
        screen.fill((255, 255, 255))  # Clear the screen
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
        screen.blit(game_over_text, (screen_width // 2 - 150, screen_height // 2 - 50))
        screen.blit(score_text, (screen_width // 2 - 100, screen_height // 2 + 50))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False
        continue
#######
    now = pygame.time.get_ticks()
    if now - last_frame_time > frame_duration:
        current_frame = (current_frame + 1) % len(theface)
        last_frame_time = now
    frame_rect = theface[current_frame].get_rect(center=(screen_width // 2, screen_height // 2 - 150))
    screen.blit(theface[current_frame], frame_rect)
    for hole in holes:
        pygame.draw.circle(screen, (200, 200, 200), hole, 50)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    umbrella_rect = umbrella_img.get_rect(center=(mouse_x, mouse_y))
    screen.blit(umbrella_img, umbrella_rect)
    if fly_visible and fly_position:
        fly_rect = fly_img.get_rect(center=fly_position)
        screen.blit(fly_img, fly_rect)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    ####  6
    remaining_time = max(0, (game_time_limit - elapsed_time) // 1000)  # Convert to seconds
    time_text = font.render(f"Time Left: {remaining_time}s", True, (0, 0, 0))
    screen.blit(time_text, (screen_width - 200, 10))
    ####
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            if not fly_visible:
                fly_position = random.choice(holes)
                fly_visible = True
                pygame.time.set_timer(pygame.USEREVENT + 1, fly_duration)
            else:
                fly_visible = False
                fly_position = None
                pygame.time.set_timer(pygame.USEREVENT, fly_appearance_time)
        elif event.type == pygame.USEREVENT + 1:
            fly_visible = False
            fly_position = None
            pygame.time.set_timer(pygame.USEREVENT, fly_appearance_time)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if fly_visible and fly_position:
                fly_rect = fly_img.get_rect(center=fly_position)
                if fly_rect.collidepoint(event.pos):  # Check if click is within the fly's rectangle
                    fly_visible = False  # Hide the fly if clicked
                    fly_position = None
                    score += 1
                    pygame.time.set_timer(pygame.USEREVENT, fly_appearance_time)
    pygame.display.flip()
pygame.quit()
sys.exit()
