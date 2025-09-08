import pygame, sys, os

pygame.init()
W, H = 640, 360
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Player Movement (Bounded)")

BLACK = (0, 0, 0)

ASSET_DIR = "assets"
PLAYER_IMG = os.path.join(ASSET_DIR, "player.png")

# load and scale player
player_img = pygame.image.load(PLAYER_IMG).convert_alpha()
player_img = pygame.transform.smoothscale(player_img, (100, 160))

player_rect = player_img.get_rect(center=(W // 2, H // 2))
world_bounds = pygame.Rect(0, 0, W, H)  # screen bounds

clock = pygame.time.Clock()
speed = 5

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    # movement with arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  player_rect.x -= speed
    if keys[pygame.K_RIGHT]: player_rect.x += speed
    if keys[pygame.K_UP]:    player_rect.y -= speed
    if keys[pygame.K_DOWN]:  player_rect.y += speed

    # keep player on screen
    player_rect.clamp_ip(world_bounds)

    # draw
    screen.fill(BLACK)
    screen.blit(player_img, player_rect)
    pygame.display.flip()
    clock.tick(60)
