import pygame
from game.sprite import NPC

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Loowit Sprite Example")

# Create sprite instance
loowit = NPC(400, 300)
all_sprites = pygame.sprite.Group(loowit)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((100, 200, 180))  # ocean-like background
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
