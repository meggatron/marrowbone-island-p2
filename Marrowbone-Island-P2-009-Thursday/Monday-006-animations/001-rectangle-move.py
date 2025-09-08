import pygame, sys

pygame.init()
W, H = 640, 360
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Single Rectangle")

BLACK = (0, 0, 0)
RED   = (255, 0, 0)

# A 100x160 rectangle centered on screen
rect_w, rect_h = 100, 160
# make a Rect at (0,0) with width=rect_w and height=rect_h
rect = pygame.Rect(0, 0, rect_w, rect_h)
rect.center = (W // 2, H // 2)

clock = pygame.time.Clock()
speed = 5  # pixels per frame

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    # --- movement with arrow keys ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rect.x -= speed
    if keys[pygame.K_RIGHT]:
        rect.x += speed
    if keys[pygame.K_UP]:
        rect.y -= speed
    if keys[pygame.K_DOWN]:
        rect.y += speed

    # --- draw ---
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, rect)
    pygame.display.flip()
    clock.tick(60)
