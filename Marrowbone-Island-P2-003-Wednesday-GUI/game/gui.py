import pygame

pygame.init()
screen = pygame.display.get_surface()
if screen is None:
    screen = pygame.display.set_mode((800, 600))

font = pygame.font.SysFont("Arial", 24)

def display(text):
    if isinstance(text, str):
        lines = text.split('\n')
    else:
        lines = text

    screen.fill((10, 20, 40))
    for i, line in enumerate(lines):
        line_surface = font.render(line, True, pygame.Color(255, 255, 255))
        screen.blit(line_surface, (20, 30 + i * 30))
    pygame.display.flip()

def get_input(prompt):
    if isinstance(prompt, str):
        lines = prompt.split('\n')
    else:
        lines = prompt

    input_text = ""
    active = True
    while active:
        screen.fill((10, 20, 40))

        # Draw prompt lines
        for i, line in enumerate(lines):
            line_surface = font.render(line, True, pygame.Color(255, 255, 255))
            screen.blit(line_surface, (20, 30 + i * 30))

        # Draw input field
        input_surface = font.render("> " + input_text, True, pygame.Color(0, 255, 0))
        screen.blit(input_surface, (20, 40 + len(lines) * 30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    return input_text.strip()

def pause(ms):
    pygame.time.wait(ms)
