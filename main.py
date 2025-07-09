import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH = 400  # ✅ Added missing WIDTH definition
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load and scale background image
bg_img = pygame.image.load("assets/bg.png").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
bg_x = 0

# Load and scale bird image
bird_img = pygame.image.load("assets/bird.png")
bird_img = pygame.transform.scale(bird_img, (80, 55))

# Fonts
font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 24)

# Clock
clock = pygame.time.Clock()

# Bird properties
bird_x = 50
bird_y = 300
bird_radius = 20
velocity = 0
gravity = 0.5
jump_power = -10

# Pipe properties
pipe_width = 70
pipe_gap = 150
pipe_x = WIDTH
pipe_height = 300

# Score tracking
score = 0
scored = False

def welcome_screen():
    button_rect = pygame.Rect(WIDTH // 2 - 60, 320, 120, 50)
    waiting = True
    while waiting:
        screen.fill((135, 206, 250))

        title = font.render("Flappy Bird", True, (255, 255, 255))
        quote = small_font.render("Press SPACE or TAP to flap!", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 180))
        screen.blit(quote, (WIDTH // 2 - quote.get_width() // 2, 230))

        screen.blit(bird_img, (WIDTH // 2 - 30, 270))

        pygame.draw.rect(screen, (0, 0, 0), button_rect, border_radius=8)
        btn_text = font.render("START", True, (255, 255, 255))
        screen.blit(btn_text, (button_rect.centerx - btn_text.get_width() // 2,
                               button_rect.centery - btn_text.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False
    return

def game_loop():
    global bird_x, bird_y, velocity, pipe_x, pipe_height, score, scored, bg_x
    bird_y = 300
    velocity = 0
    pipe_x = WIDTH
    pipe_height = 300
    score = 0
    scored = False
    intro_bird_x = bird_x

    # --- Intro phase ---
    intro_running = True
    alpha = 0
    float_offset = 0
    float_direction = 1
    intro_start_time = pygame.time.get_ticks()

    while intro_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                intro_running = False
                velocity = jump_power
                pipe_delay_timer = pygame.time.get_ticks()
            if event.type == pygame.MOUSEBUTTONDOWN:
                intro_running = False
                velocity = jump_power
                pipe_delay_timer = pygame.time.get_ticks()

        bg_x -= 1
        if bg_x <= -WIDTH:
            bg_x = 0
        screen.blit(bg_img, (bg_x, 0))
        screen.blit(bg_img, (bg_x + WIDTH, 0))

        # Floating bobbing
        if float_direction == 1:
            float_offset += 0.5
            if float_offset > 8:
                float_direction = -1
        else:
            float_offset -= 0.5
            if float_offset < -8:
                float_direction = 1

        intro_bird_x += 1
        screen.blit(bird_img, (intro_bird_x, int(bird_y + float_offset)))

        if alpha < 255:
            alpha += 4
        ready_text = font.render("Ready? Tap or Press SPACE", True, (255, 255, 255))
        ready_text.set_alpha(alpha)
        screen.blit(ready_text, (WIDTH // 2 - ready_text.get_width() // 2, 200))

        pygame.display.flip()
        clock.tick(60)

    # --- Main Game Loop ---
    pipe_visible = False
    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                velocity = jump_power
            if event.type == pygame.MOUSEBUTTONDOWN:
                velocity = jump_power

        velocity += gravity
        bird_y += velocity

        if not pipe_visible:
            if pygame.time.get_ticks() - pipe_delay_timer >= 2000:
                pipe_visible = True

        if pipe_visible:
            pipe_x -= 4
            if pipe_x + pipe_width < bird_x and not scored:
                score += 1
                scored = True
            if pipe_x < -pipe_width:
                pipe_x = WIDTH
                pipe_height = random.randint(100, 400)
                scored = False

        bg_x -= 1
        if bg_x <= -WIDTH:
            bg_x = 0
        screen.blit(bg_img, (bg_x, 0))
        screen.blit(bg_img, (bg_x + WIDTH, 0))

        screen.blit(bird_img, (bird_x, int(bird_y)))

        if pipe_visible:
            pygame.draw.rect(screen, (50, 50, 50), (pipe_x, 0, pipe_width, pipe_height))
            pygame.draw.rect(screen, (50, 50, 50), (pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT))

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Collision detection
        if bird_y - bird_radius < 0 or bird_y + bird_radius > HEIGHT:
            return
        if pipe_visible and (
            pipe_x < bird_x + bird_radius < pipe_x + pipe_width and
            (bird_y - bird_radius < pipe_height or bird_y + bird_radius > pipe_height + pipe_gap)
        ):
            return

        pygame.display.flip()

def game_over_screen():
    restart_rect = pygame.Rect(WIDTH // 2 - 110, 330, 100, 40)
    exit_rect = pygame.Rect(WIDTH // 2 + 10, 330, 100, 40)

    screen.fill((0, 0, 0))

    game_over_text = font.render("Game Over", True, (255, 0, 0))
    final_score_text = small_font.render(f"Final Score: {score}", True, (255, 255, 255))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 220))
    screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, 270))

    pygame.draw.rect(screen, (0, 100, 0), restart_rect, border_radius=8)
    restart_text = small_font.render("Restart", True, (255, 255, 255))
    screen.blit(restart_text, (restart_rect.centerx - restart_text.get_width() // 2,
                               restart_rect.centery - restart_text.get_height() // 2))

    pygame.draw.rect(screen, (100, 0, 0), exit_rect, border_radius=8)
    exit_text = small_font.render("Exit", True, (255, 255, 255))
    screen.blit(exit_text, (exit_rect.centerx - exit_text.get_width() // 2,
                            exit_rect.centery - exit_text.get_height() // 2))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    waiting = False
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# --- Main Loop ---
first_run = True

while True:
    if first_run:
        welcome_screen()
        first_run = False

    game_loop()
    game_over_screen()

pygame.quit()
sys.exit()
