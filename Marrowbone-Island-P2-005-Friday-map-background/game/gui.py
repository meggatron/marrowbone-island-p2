import pygame
from game import player

pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont("Arial", 24)

# NEW: ----------------------------------------------------------------------------
# Background (drawn BEFORE UI) and Overlay (drawn AFTER UI) hooks + helpers.
_bg_draw_fn = None           # NEW
_fg_draw_fn = None           # NEW

def set_background(draw_fn):
    """Register a background drawer (runs BEFORE UI). Returns previous."""  # NEW
    global _bg_draw_fn        # NEW
    prev = _bg_draw_fn        # NEW
    _bg_draw_fn = draw_fn     # NEW
    return prev               # NEW

def set_overlay(draw_fn):
    """Register an overlay drawer (runs AFTER UI). Returns previous."""     # NEW
    global _fg_draw_fn        # NEW
    prev = _fg_draw_fn        # NEW
    _fg_draw_fn = draw_fn     # NEW
    return prev               # NEW

def _maybe_background():      # NEW
    """Draw background first (if any)."""                                  # NEW
    if _bg_draw_fn:            # NEW
        dest = pygame.display.get_surface() or screen   # NEW
        _bg_draw_fn(dest)      # NEW

def present():                # NEW
    """Draw overlay last (if any), then flip the frame."""                  # NEW
    if _fg_draw_fn:            # NEW
        dest = pygame.display.get_surface() or screen   # NEW
        _fg_draw_fn(dest)      # NEW
    pygame.display.flip()      # NEW
# -------------------------------------------------------------------------------

def draw_status():
    """Top status bar."""
    # CHANGED: only clear a header strip if a background is active;
    # otherwise clear the whole screen (legacy behavior).
    try:
        bg_active = _bg_draw_fn is not None   # requires today's gui.py with hooks
    except NameError:
        bg_active = False

    if bg_active:
        # Draw a header bar so background stays visible.
        bar_h = 80
        pygame.draw.rect(screen, (10, 20, 40), (0, 0, screen.get_width(), bar_h))
    else:
        # No background → clear whole screen like before.
        screen.fill((10, 20, 40))

    inventory_text = f"Inventory: {', '.join(player.inventory) if player.inventory else 'None'}"
    gifts_text     = f"Gifts: {', '.join(player.gifts) if player.gifts else 'None'}"
    npcs_text      = f"NPCs Met: {', '.join(player.npcs) if player.npcs else 'None'}"

    for i, line in enumerate([inventory_text, gifts_text, npcs_text]):
        line_surface = font.render(line, True, pygame.Color("white"))
        screen.blit(line_surface, (20, 5 + i * 25))


def display(text):
    """Display main text, preserving status bar."""
    if isinstance(text, str):
        lines = text.strip().split('\n')
    else:
        lines = text

    _maybe_background()        # NEW: draw background FIRST (if any)
    draw_status()              # (then UI/status)

    for i, line in enumerate(lines):
        line_surface = font.render(line, True, pygame.Color("white"))
        screen.blit(line_surface, (20, 100 + i * 30))

    present()                  # CHANGED: was pygame.display.flip(); now present() so overlay draws LAST


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
        _maybe_background()    # NEW: draw background FIRST each frame
        draw_status()

        for i, line in enumerate(lines):
            line_surface = font.render(line, True, pygame.Color("white"))
            screen.blit(line_surface, (20, 100 + i * 30))

        input_surface = font.render("> " + input_text, True, pygame.Color("lime"))
        screen.blit(input_surface, (20, 120 + len(lines) * 30))

        present()              # CHANGED: was pygame.display.flip(); now present() so overlay draws LAST

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
                    # CHANGED: guard to accept printable chars only (safer for inputs)
                    if event.unicode and event.unicode.isprintable():
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
        # NEW: light refresh so background/overlay stay visible during pauses
        _maybe_background()    # NEW
        draw_status()          # NEW
        present()              # NEW
        clock.tick(30)
        elapsed += clock.get_time()
