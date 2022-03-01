import random
import time

import pygame
import math

width = 805
height = 500
status = "start"
pygame.init()
sc = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
img = pygame.image.load("fon.jpg").convert()
font = pygame.font.Font(None, 48)

def start():
    global width, height
    global fps, platform_w, platform_h, platform_speed, platform, ball_rect, \
        ball_r, ball_speed, dx, dy, ball, blocks, colors
    fps = 60
    platform_w = 150
    platform_h = 25
    platform_speed = 11
    platform = pygame.Rect(width // 2 - platform_w // 2, height - platform_h - 10, platform_w, platform_h)
    ball_r = 10
    ball_speed = 3
    ball_rect = math.floor(math.sqrt(ball_r * 2))
    dx, dy = 1, -1
    ball = pygame.Rect(random.randint(10, width - 10), height // 2, ball_rect, ball_rect)
    blocks = [pygame.Rect(5 + 80 * i, 10 + 70 * j, 75, 25) for i in range(10) for j in range(4)]
    colors = [random.choice(["green", "purple", "blue"]) for i in range(40)]


def check(dx, dy, ball, rect):
    if dx > 0:
        deltax = ball.right - rect.left
    else:
        deltax = rect.right - ball.left
    if dy > 0:
        deltay = ball.bottom - rect.top
    else:
        deltay = rect.bottom - ball.top
    if abs(deltax-deltay) < 7:
        dx *= -1
        dy *= -1
    elif deltax > deltay:
        dy *= -1
    elif deltay > deltax:
        dx *= -1
    return dx, dy


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.blit(img, (0,0))
    if status == "start":
        start()
        status = "playing"
    elif status == "playing":
        pygame.draw.circle(sc, pygame.Color("yellow"), ball.center, ball_r)
        pygame.draw.rect(sc, pygame.Color('white'), platform)
        [pygame.draw.rect(sc, colors[blocks.index(block)], block) for block in blocks]
    elif status == "gg":
        text = font.render("YOU LOSE. CLICK R", True, (0, 180, 0))
        sc.blit(text, (10, 50))
    elif status == "win":
        text = font.render("YOU WIN! CLICK R", True, (0, 180, 0))
        sc.blit(text, (10, 50))
    if ball.centerx < ball_r:
        ball.x += ball_speed * dx
        dx = 1
    elif ball.centerx > width - ball_r:
        dx = -1
    if ball.centery < ball_r:
        dy = 1
    if ball.colliderect(platform) and dy > 0:
        dx, dy = check(dx, dy, ball, platform)
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
    index = ball.collidelist(blocks)
    if index != -1:
        rect = blocks.pop(index)
        color = colors.pop(index)
        dx, dy = check(dx, dy, ball, rect)
        ball_speed += 0.1
    if ball.bottom > height:
        blocks = []
        colors = []
        [pygame.draw.rect(sc, colors[blocks.index(block)], block) for block in blocks]
        status = "gg"
    if len(blocks) == 0 and status != "gg":
        status = "win"
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and platform.left + platform_w <= 0:
        platform.left = width - platform_speed
    if key[pygame.K_LEFT]:
        platform.left -= platform_speed
    if key[pygame.K_RIGHT] and platform.right >= width:
        platform.right = 0
    if key[pygame.K_RIGHT]:
        platform.right += platform_speed
    if key[pygame.K_r]:
        status = "start"
        time.sleep(0.5)
    pygame.display.flip()
    clock.tick(fps)
