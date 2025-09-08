# game/gui.py
# minimal gui helpers that draw text and read input; functions take a player (no globals)
# Status (inventory / gifts / npcs) renders at the top.
# Main page look: sky-blue background, brown ground at bottom, player on right,
# semi-transparent island mini-map in the upper-left.

import os
import sys
import pygame

# -------- visual constants --------
_TOP_MARGIN   = 12
_LINE_SP      = 25
_SECTION_GAP  = 10

SKY           = (135, 206, 235)
GROUND        = (139, 108, 78)
SKY_TEXT      = (75, 55, 40)     # brown-ish ink over blue sky
GROUND_TEXT   = (245, 240, 230)  # light ink over brown ground

_ASSET_DIR    = "assets"
_PLAYER_FILE  = "player.png"
_ISLAND_FILE  = "island.jpg"     # source for the HUD mini-map

# cached surfaces (scaled to current window)
_player_img: pygame.Surface | None = None
_player_h_for: int | None = None
_island_img: pygame.Surface | None = None
_island_w_for: int | None = None


# ---------- internals ----------
def _draw_background_and_hud():
    """
    Paint sky + ground, then blit the player (right) and the mini-map (upper-left).
    Returns (ground_top, player_rect or None).
    """
    global _player_img, _player_h_for, _island_img, _island_w_for

    screen = pygame.display.get_surface()
    if screen is None:
        return 0, None

    W, H = screen.get_size()
    ground_h   = max(90, int(H * 0.18))
    ground_top = H - ground_h

    # background layers
    screen.fill(SKY)
    pygame.draw.rect(screen, GROUND, (0, ground_top, W, ground_h))

    # player (right side)
    pr = None
    if (_player_img is None) or (_player_h_for != H):
        try:
            img = pygame.image.load(os.path.join(_ASSET_DIR, _PLAYER_FILE)).convert_alpha()
            target_h = int(H * 0.55)
            w, h = img.get_size()
            s = target_h / max(1, h)
            _player_img = pygame.transform.smoothscale(img, (int(w * s), int(h * s)))
            _player_h_for = H
        except Exception:
            _player_img = None

    if _player_img:
        pr = _player_img.get_rect()
        pr.bottom = H - 4
        pr.right  = W - int(W * 0.06)
        screen.blit(_player_img, pr.topleft)

    # mini-map (upper-left, ~1/6 screen width, semi-transparent)
    target_w = max(120, W // 6)
    if (_island_img is None) or (_island_w_for != target_w):
        try:
            base = pygame.image.load(os.path.join(_ASSET_DIR, _ISLAND_FILE)).convert_alpha()
            scale = target_w / max(1, base.get_width())
            target_h = int(base.get_height() * scale)
            _island_img = pygame.transform.smoothscale(base, (target_w, target_h))
            _island_w_for = target_w
            _island_img.set_alpha(140)  # 0 transparent .. 255 opaque
        except Exception:
            _island_img = None

    if _island_img:
        screen.blit(_island_img, (10, 10))

    return ground_top, pr


def _ink_for_y(y: int, ground_top: int) -> tuple[int, int, int]:
    """Readable ink color chosen by whether the baseline sits on sky or ground."""
    return SKY_TEXT if y < ground_top else GROUND_TEXT


def _render_line(screen, font, text, x, y, ground_top):
    """Render/blit one line with auto ink based on background at that y."""
    color = _ink_for_y(y, ground_top)
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))
    return y + _LINE_SP


# ---------- public helpers ----------
def draw_status(player):
    """
    Clear/paint the main page (sky, ground, player, mini-map), then draw status lines.
    Returns the y-position where scene text should begin.
    """
    screen = pygame.display.get_surface()
    if screen is None:
        return _TOP_MARGIN

    font = pygame.font.SysFont("arial", 24)

    ground_top, _ = _draw_background_and_hud()

    inv   = f"inventory: {', '.join(player.inventory) if player.inventory else 'none'}"
    gifts = f"gifts: {', '.join(player.gifts) if player.gifts else 'none'}"
    npcs  = f"npcs met: {', '.join(player.npcs) if player.npcs else 'none'}"

    y = _TOP_MARGIN
    y = _render_line(screen, font, inv,   20, y, ground_top)
    y = _render_line(screen, font, gifts, 20, y, ground_top)
    y = _render_line(screen, font, npcs,  20, y, ground_top)
    y += _SECTION_GAP
    return y


def display(text, player):
    """
    Render one or more lines of scene text.
    Accepts a single string (with '\n') or an iterable of strings.
    """
    screen = pygame.display.get_surface()
    if screen is None:
        return
    font = pygame.font.SysFont("arial", 24)

    # normalize to list of lines
    lines = text.strip().split('\n') if isinstance(text, str) else list(text)

    # prepare background + status once per call
    ground_top, _ = _draw_background_and_hud()
    y = _TOP_MARGIN
    # status block
    inv   = f"inventory: {', '.join(player.inventory) if player.inventory else 'none'}"
    gifts = f"gifts: {', '.join(player.gifts) if player.gifts else 'none'}"
    npcs  = f"npcs met: {', '.join(player.npcs) if player.npcs else 'none'}"
    y = _render_line(screen, font, inv,   20, y, ground_top)
    y = _render_line(screen, font, gifts, 20, y, ground_top)
    y = _render_line(screen, font, npcs,  20, y, ground_top)
    y += _SECTION_GAP

    # body text
    for line in lines:
        y = _render_line(screen, font, line, 20, y, ground_top)

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
    lines = prompt.strip().split('\n') if isinstance(prompt, str) else list(prompt)

    input_text = ""
    active = True
    clock = pygame.time.Clock()

    while active:
        ground_top, _ = _draw_background_and_hud()

        # draw prompt lines
        y = _TOP_MARGIN
        inv   = f"inventory: {', '.join(player.inventory) if player.inventory else 'none'}"
        gifts = f"gifts: {', '.join(player.gifts) if player.gifts else 'none'}"
        npcs  = f"npcs met: {', '.join(player.npcs) if player.npcs else 'none'}"
        y = _render_line(screen, font, inv,   20, y, ground_top)
        y = _render_line(screen, font, gifts, 20, y, ground_top)
        y = _render_line(screen, font, npcs,  20, y, ground_top)
        y += _SECTION_GAP

        for line in lines:
            y = _render_line(screen, font, line, 20, y, ground_top)

        # live input line
        y += 20
        ink = _ink_for_y(y, ground_top)
        surf = font.render("> " + input_text, True, ink)
        screen.blit(surf, (20, y))

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
                    input_text += e.unicode

        clock.tick(30)

    return input_text.strip()


def pause(ms):
    """Pause while still processing QUIT events (so the window remains responsive)."""
    clock = pygame.time.Clock()
    elapsed = 0
    while elapsed < ms:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        dt = clock.tick(30)
        elapsed += dt
