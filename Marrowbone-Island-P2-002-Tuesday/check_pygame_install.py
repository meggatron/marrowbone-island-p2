import pygame

print(f"pygame version: {pygame.__version__}")
pygame.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("pygame check")
screen.fill((30, 30, 30))
pygame.display.flip()

print("pygame window opened — close it to finish.")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
