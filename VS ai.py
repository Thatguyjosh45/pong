import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ball settings
BALL_SPEED = 5
BALL_SIZE = 15

# Paddle settings
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Ball position and velocity
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_dx = BALL_SPEED
ball_dy = BALL_SPEED

# Paddle positions
player1_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
player2_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2

# Scores
player1_score = 0
player2_score = 0

# Font
font = pygame.font.Font(None, 36)

def draw_objects():
    screen.fill(BLACK)

    # Draw ball
    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    # Draw paddles
    pygame.draw.rect(screen, WHITE, (20, player1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - 30, player2_y, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw scores
    player1_text = font.render(str(player1_score), True, WHITE)
    player2_text = font.render(str(player2_score), True, WHITE)
    screen.blit(player1_text, (SCREEN_WIDTH // 4, 20))
    screen.blit(player2_text, (SCREEN_WIDTH * 3 // 4, 20))

def handle_ball_movement():
    global ball_x, ball_y, ball_dx, ball_dy, player1_score, player2_score

    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collision with top and bottom walls
    if ball_y <= 0 or ball_y >= SCREEN_HEIGHT - BALL_SIZE:
        ball_dy = -ball_dy

    # Ball collision with paddles
    if (ball_x <= 30 and player1_y <= ball_y <= player1_y + PADDLE_HEIGHT) or \
       (ball_x >= SCREEN_WIDTH - 30 - BALL_SIZE and player2_y <= ball_y <= player2_y + PADDLE_HEIGHT):
        ball_dx = -ball_dx

    # Ball out of bounds
    if ball_x < 0:
        player2_score += 1
        reset_ball()
    elif ball_x > SCREEN_WIDTH:
        player1_score += 1
        reset_ball()

def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    ball_dx = BALL_SPEED if ball_dx < 0 else -BALL_SPEED
    ball_dy = BALL_SPEED if ball_dy < 0 else -BALL_SPEED

def handle_paddle_movement(keys):
    global player1_y

    # Player 1 controls (W/S)
    if keys[pygame.K_w] and player1_y > 0:
        player1_y -= PADDLE_SPEED
    if keys[pygame.K_s] and player1_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
        player1_y += PADDLE_SPEED

def ai_paddle_movement():
    global player2_y

    # AI Paddle movement
    if player2_y + PADDLE_HEIGHT / 2 < ball_y:
        player2_y += PADDLE_SPEED
    elif player2_y + PADDLE_HEIGHT / 2 > ball_y:
        player2_y -= PADDLE_SPEED

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle paddle movement
    keys = pygame.key.get_pressed()
    handle_paddle_movement(keys)

    # Handle ball movement
    handle_ball_movement()

    # AI Paddle movement
    ai_paddle_movement()

    # Draw everything
    draw_objects()

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
