import pygame
from game.sprite import NPC

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Creature")
clock = pygame.time.Clock()

# create sprite instance
orca = NPC(400, 300)
all_sprites = pygame.sprite.Group(orca)

# world bounds for clamping movement (match window size)
BOUNDS = screen.get_rect()

running = True
while running:
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # input: arrow keys for movement
    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_LEFT]:
        dx -= orca.speed
    if keys[pygame.K_RIGHT]:
        dx += orca.speed
    if keys[pygame.K_UP]:
        dy -= orca.speed
    if keys[pygame.K_DOWN]:
        dy += orca.speed
    if dx or dy:
        orca.move(dx, dy, bounds=BOUNDS)

    # update
    all_sprites.update()  # advances animation frames

    # draw
    screen.fill((100, 200, 180))  # ocean blue background
    all_sprites.draw(screen)
    pygame.display.flip()

    # cap frames per second
    clock.tick(60)

pygame.quit()
