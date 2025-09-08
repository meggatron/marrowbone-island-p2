# game/gui.py
# minimal gui helpers that draw text and read input; functions take a player (no globals)
# Backpack UI removed — inventory/gifts/npcs are always visible at the top.

import pygame, sys

# vertical spacing constants for readability
_TOP_MARGIN = 12
_LINE_SP   = 25
_BODY_SP   = 30
_SECTION_GAP = 10


def _render_line(screen, font, text, x, y, color="white"):
    """Small helper so we don't repeat render/blit boilerplate."""
    surf = font.render(text, True, pygame.Color(color))
    screen.blit(surf, (x, y))
    return y + _LINE_SP


def draw_status(player):
    """
    Draw the status block (inventory / gifts / npcs) at the top.
    Returns the y-position where scene text should begin so callers don't guess.
    """
    screen = pygame.display.get_surface()
    if screen is None:
        return _TOP_MARGIN

    font = pygame.font.SysFont("arial", 24)

    # clear screen before drawing
    screen.fill((10, 20, 40))

    # compose three status lines
    inv = f"inventory: {', '.join(player.inventory) if player.inventory else 'none'}"
    gifts = f"gifts: {', '.join(player.gifts) if player.gifts else 'none'}"
    npcs = f"npcs met: {', '.join(player.npcs) if player.npcs else 'none'}"

    y = _TOP_MARGIN
    y = _render_line(screen, font, inv,   20, y)
    y = _render_line(screen, font, gifts, 20, y)
    y = _render_line(screen, font, npcs,  20, y)

    # spacer under the status block so the next section breathes
    y += _SECTION_GAP
    return y


def display(text, player):
    """
    Render one or more lines of scene text.
    Accepts either a single string (with '\n') or a list/tuple of strings.
    """
    screen = pygame.display.get_surface()
    if screen is None:
        return
    font = pygame.font.SysFont("arial", 24)

    # normalize to a list of lines
    lines = text.strip().split('\n') if isinstance(text, str) else list(text)

    y = draw_status(player)

    # body text block
    for line in lines:
        y = _render_line(screen, font, line, 20, y)

    pygame.display.flip()


def get_input(prompt, player):
    """
    Prompt the player for input with a live-typing line.
    ENTER submits. BACKSPACE deletes. Handles QUIT safely.
    """
    screen = pygame.display.get_surface()
    if screen is None:
        return ""
    font = pygame.font.SysFont("arial", 24)

    # normalize to a list of lines
    lines = prompt.strip().split('\n') if isinstance(prompt, str) else list(prompt)

    input_text = ""
    active = True
    clock = pygame.time.Clock()

    while active:
        y = draw_status(player)

        # draw prompt lines
        for line in lines:
            y = _render_line(screen, font, line, 20, y)

        # live input line (slight extra gap from the prompt)
        y += 20
        _render_line(screen, font, "> " + input_text, 20, y, color="lime")

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    active = False
                elif e.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    # accept typed characters (including spaces and punctuation)
                    input_text += e.unicode

        clock.tick(30)

    return input_text.strip()


def pause(ms):
    """
    Pause while still processing QUIT events (so the window remains responsive).
    """
    clock = pygame.time.Clock()
    elapsed = 0
    while elapsed < ms:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        clock.tick(30)
        elapsed += clock.get_time()
