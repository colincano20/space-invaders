import pygame
import random

# Initialize Pygame
pygame.init()
#(C:\Users\colin\VisStudioPy\.conda) C:\Users\colin\VisStudioPy\Space Invaders>python space_invaders.py
# Constants
WIDTH, HEIGHT = 1000, 600
FPS = 60
ALIEN_ROWS = 5
ALIEN_COLUMNS = 10
ALIEN_SPACING = 59
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 30
ALIEN_WIDTH, ALIEN_HEIGHT = 80,50
BULLET_HEIGHT = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images
spaceship_img = pygame.transform.scale(pygame.image.load("Space Invaders/spaceship.png"), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
alien_img = pygame.transform.scale(pygame.image.load("Space Invaders/alien.png"), (ALIEN_WIDTH, ALIEN_HEIGHT))

# Classes for game objects
class Spaceship:
    def __init__(self):
        self.rect = spaceship_img.get_rect(center=(WIDTH // 2, HEIGHT - 50))

    def move(self, dx):
        self.rect.x += dx
        # Keep within bounds
        self.rect.x = max(0, min(WIDTH - SPACESHIP_WIDTH, self.rect.x))

    def draw(self, surface):
        surface.blit(spaceship_img, self.rect)

class Alien:
    def __init__(self, x, y):
        self.rect = alien_img.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(alien_img, self.rect)

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, BULLET_HEIGHT)

    def move(self):
        self.rect.y -= 10

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.rect)

# Initialize game objects
spaceship = Spaceship()
aliens = [Alien(x * ALIEN_SPACING + 100, y * ALIEN_SPACING + 50) for y in range(ALIEN_ROWS) for x in range(ALIEN_COLUMNS)]
bullets = []

# Game variables
score = 0
level = 1
game_over = False
win = False
alien_direction = 1  # 1 for right, -1 for left
clock = pygame.time.Clock()
alien_drop_counter = 0  # Counter for alien drops
alien_drop_interval = 30  # Counter threshold to drop aliens


def reset_game():
    global level, aliens, bullets, alien_direction
    level = 1
    aliens = [Alien(x * ALIEN_SPACING + 100, y * ALIEN_SPACING + 50) for y in range(ALIEN_ROWS) for x in range(ALIEN_COLUMNS)]
    bullets.clear()
    alien_direction = 1  # Reset alien direction
   


# Game loop
running = True




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if not game_over and not win:
        if keys[pygame.K_LEFT]:
            spaceship.move(-5)
        if keys[pygame.K_RIGHT]:
            spaceship.move(5)
        if keys[pygame.K_SPACE]:
        # Fire bullet
            bullets.append(Bullet(spaceship.rect.centerx - 2.5, spaceship.rect.top))

 

    # Move bullets
    for bullet in bullets[:]:
        bullet.move()
        if bullet.rect.y < 0:
            bullets.remove(bullet)

    # Check for bullet collision with aliens
    for bullet in bullets[:]:
        for alien in aliens[:]:
            if bullet.rect.colliderect(alien.rect):
                bullets.remove(bullet)
                aliens.remove(alien)
                score += 10
                break
    # Move aliens
    if aliens:
        for alien in aliens:
            alien.rect.x += alien_direction  # Move aliens horizontally
        # Change direction if alien hits edge
        if aliens[0].rect.x <= 0 or aliens[-1].rect.x >= WIDTH - SPACESHIP_WIDTH:
            alien_direction *= -1  # Reverse direction
        if alien_drop_counter >= alien_drop_interval:
            for alien in aliens:
                alien.rect.y += 10  # Move down
            alien_drop_counter = 0  # Reset drop counter

        # Check if any alien has reached the bottom
        if any(alien.rect.y >= HEIGHT - SPACESHIP_HEIGHT for alien in aliens):
            game_over = True

    # Check win condition and level up
    if not aliens and not win:
        level += 1
        ALIEN_ROWS += 1  # Increase the number of rows for the next level
        ALIEN_COLUMNS += 1  # Increase the number of columns for the next level
        # Reset aliens for the next level
        aliens = [Alien(x * ALIEN_SPACING + 100, y * ALIEN_SPACING + 50) for y in range(ALIEN_ROWS) for x in range(ALIEN_COLUMNS)]

        alien_drop_interval = max(10, alien_drop_interval - 5)  # Increase speed of alien drop

    # Draw everything
    screen.fill(BLACK)
    spaceship.draw(screen)
    for alien in aliens:
        alien.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)

    # Display score and level
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    # Game Over message
    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
    elif win:
        win_text = font.render("You Win! Press R to Restart", True, GREEN)
        screen.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2))
 
 
 
    pygame.display.flip()
    clock.tick(FPS)


    # Restart the game
    if (game_over or win) and keys[pygame.K_r]:
        game_over = False
        win = False
        score = 0
        alien_direction = 1  # Reset alien direction
        aliens = [Alien(x * ALIEN_SPACING + 100, y * ALIEN_SPACING + 50) for y in range(ALIEN_ROWS) for x in range(ALIEN_COLUMNS)]
        bullets.clear()





pygame.quit()
