import pygame

def display(text):
    screen = pygame.display.get_surface()
    font = pygame.font.SysFont(None, 20)
    screen.fill(pygame.Color(20,30,50))

    if isinstance(text, str):
        lines = text.split("\n")
    elif isinstance(text, list):
        lines = text
    else:
        raise ValueError("gui.display() expects a string or list of strings.")

    for i, line in enumerate(lines):
        rendered_line = font.render(line, True, pygame.Color(255,200,200))
        screen.blit(rendered_line, (50, 100 + i*30))

    pygame.display.flip()

def get_input(prompt=">"):
    screen = pygame.display.get_surface()
    font = pygame.font.SysFont(None, 28)
    clock = pygame.time.Clock()

    input_text = ""
    active = True

    while active:
        screen.fill(pygame.Color(20, 30, 50))

        prompt_surface = font.render(prompt, True, pygame.Color(255, 255, 255))
        screen.blit(prompt_surface, (50, 100))

        input_surface = font.render(input_text, True, pygame.Color(200, 255, 200))
        screen.blit(input_surface, (50, 150))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        clock.tick(30)

    return input_text

def pause(milliseconds):
    clock = pygame.time.Clock()
    elapsed = 0
    while elapsed < milliseconds:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        clock.tick(30)
        elapsed += clock.get_time()



