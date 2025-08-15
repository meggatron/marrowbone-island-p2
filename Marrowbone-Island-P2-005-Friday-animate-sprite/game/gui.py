import pygame
from game import player

pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont("Arial", 24)

def draw_status():
    # Draw persistent status bar at the top of the screen.
    screen.fill((10, 20, 40))  # Clear screen before drawing

    inventory_text = f"Inventory: {', '.join(player.inventory) if player.inventory else 'None'}"
    gifts_text = f"Gifts: {', '.join(player.gifts) if player.gifts else 'None'}"
    npcs_text = f"NPCs Met: {', '.join(player.npcs) if player.npcs else 'None'}"

    for i, line in enumerate([inventory_text, gifts_text, npcs_text]):
        line_surface = font.render(line, True, pygame.Color("white"))
        screen.blit(line_surface, (20, 5 + i * 25))

def display(text):
    """Display main text, preserving status bar."""
    if isinstance(text, str):
        lines = text.strip().split('\n')
    else:
        lines = text

    draw_status()
    for i, line in enumerate(lines):
        line_surface = font.render(line, True, pygame.Color("white"))
        screen.blit(line_surface, (20, 100 + i * 30))
    pygame.display.flip()

def get_input(prompt):
    """Prompt user for input, preserving status bar."""
    if isinstance(prompt, str):
        lines = prompt.strip().split('\n')
    else:
        lines = prompt

    input_text = ""
    active = True
    clock = pygame.time.Clock()

    while active:
        draw_status()

        for i, line in enumerate(lines):
            line_surface = font.render(line, True, pygame.Color("white"))
            screen.blit(line_surface, (20, 100 + i * 30))

        input_surface = font.render("> " + input_text, True, pygame.Color("lime"))
        screen.blit(input_surface, (20, 120 + len(lines) * 30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        clock.tick(30)

    return input_text.strip()

def pause(ms):
    """Pause but keep the window responsive."""
    clock = pygame.time.Clock()
    elapsed = 0
    while elapsed < ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        clock.tick(30)
        elapsed += clock.get_time()
