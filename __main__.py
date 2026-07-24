import pygame as pg
import sys
import random

WIDTH, HEIGHT = 800, 500
HUD_HEIGHT = 70
FPS = 60

BALL_SIZE = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 4

PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 6

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Ping Pong")
clock = pg.time.Clock()
font = pg.font.SysFont("Arial", 30)

ball = pg.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)

ball_dx = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
ball_dy = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])

left_paddle = pg.Rect(30, HUD_HEIGHT + 20, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pg.Rect(WIDTH - 45, HUD_HEIGHT + 20, PADDLE_WIDTH, PADDLE_HEIGHT)

score_left = 0
score_right = 0

def reset_ball(direction):
    global ball_dx, ball_dy
    ball.center = (WIDTH // 2, HUD_HEIGHT + (HEIGHT - HUD_HEIGHT) // 2)
    ball_dx = BALL_SPEED_X * direction
    ball_dy = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])
    if ball_dy == 0:
        ball_dy = BALL_SPEED_Y

def clamp_paddles():
    left_paddle.top = max(HUD_HEIGHT, left_paddle.top)
    left_paddle.bottom = min(HEIGHT, left_paddle.bottom)
    right_paddle.top = max(HUD_HEIGHT, right_paddle.top)
    right_paddle.bottom = min(HEIGHT, right_paddle.bottom)

def paddle_bounce(paddle):
    global ball_dx, ball_dy
    if ball_dx < 0:
        ball.left = paddle.right
    else:
        ball.right = paddle.left
    ball_dx *= -1
    offset = (ball.centery - paddle.centery) / (PADDLE_HEIGHT / 2)
    ball_dy = int(offset * BALL_SPEED_Y * 1.5)
    if ball_dy == 0:
        ball_dy = random.choice([-1, 1])

while True:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        left_paddle.y -= PADDLE_SPEED
    if keys[pg.K_s]:
        left_paddle.y += PADDLE_SPEED
    if keys[pg.K_UP]:
        right_paddle.y -= PADDLE_SPEED
    if keys[pg.K_DOWN]:
        right_paddle.y += PADDLE_SPEED

    clamp_paddles()

    ball.x += ball_dx
    ball.y += ball_dy

    if ball.top <= HUD_HEIGHT:
        ball.top = HUD_HEIGHT
        ball_dy *= -1

    if ball.bottom >= HEIGHT:
        ball.bottom = HEIGHT
        ball_dy *= -1

    if ball_dx < 0 and ball.colliderect(left_paddle):
        paddle_bounce(left_paddle)

    if ball_dx > 0 and ball.colliderect(right_paddle):
        paddle_bounce(right_paddle)

    if ball.right < 0:
        score_right += 1
        reset_ball(1)

    if ball.left > WIDTH:
        score_left += 1
        reset_ball(-1)

    pg.draw.line(screen, WHITE, (0, HUD_HEIGHT), (WIDTH, HUD_HEIGHT), 3)

    score_text = font.render(
        f"{score_left}  :  {score_right}",
        True,
        WHITE
    )
    screen.blit(score_text,
                (WIDTH // 2 - score_text.get_width() // 2, 20))

    pg.draw.rect(screen, WHITE, left_paddle)
    pg.draw.rect(screen, WHITE, right_paddle)
    pg.draw.ellipse(screen, WHITE, ball)

    pg.display.flip()
