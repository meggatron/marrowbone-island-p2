import pygame
from game import gui

def tide_pools():
    """Orca scene: full-screen map background + movable, on-move animation (+ sound)."""
    screen = pygame.display.get_surface() or pygame.display.set_mode((800, 600))

    # NEW: SOUND
    # freesound.org is a great resource for audio
    try:
        if not pygame.mixer.get_init():  # NEW: safe init only if needed
            pygame.mixer.pre_init(44100, -16, 2, 512)  # NEW: lower latency buffer
            pygame.mixer.init()
        orca_sound = pygame.mixer.Sound("assets/orcas.wav")  # NEW
    except Exception as e:
        orca_sound = None
        print(f"[WARN] Could not load orca sound: {e}")

    # NEW: FULL-SCREEN BACKGROUND MAP
    try:
        bg = pygame.image.load("assets/map.jpg").convert_alpha()
        bg = pygame.transform.smoothscale(bg, (screen.get_width(), screen.get_height()))  # NEW: full screen
    except Exception:
        bg = None

    def draw_full_map(dest):
        if bg:
            dest.blit(bg, (0, 0))

    # NEW: PRESERVE ORCA ASPECT RATIO & FIXED SQUISH ISSUE
    orca1 = orca2 = None
    try:
        orca1 = pygame.image.load("assets/orca.png").convert_alpha()
        orca2 = pygame.image.load("assets/orca-glow.png").convert_alpha()

        target_w = int(screen.get_width() * 0.18)  # NEW: scale based on width only
        if orca1.get_width() > target_w:
            r1 = target_w / orca1.get_width()
            orca1 = pygame.transform.smoothscale(
                orca1, (target_w, int(orca1.get_height() * r1))
            )
        if orca2.get_width() > target_w:
            r2 = target_w / orca2.get_width()
            orca2 = pygame.transform.smoothscale(
                orca2, (target_w, int(orca2.get_height() * r2))
            )
    except Exception:
        pass

    base_w = (orca1 and orca1.get_width()) or 160
    base_h = (orca1 and orca1.get_height()) or 120

    # NEW: MOVEMENT VARIABLES
    pos_x = screen.get_width() - base_w - 24
    pos_y = screen.get_height() - base_h - 24
    speed = 180  # pixels per second
    moving = False
    last_frame_swap = 0
    use_glow = False
    frame_ms = 180

    def clamp(x, y):
        x = max(0, min(screen.get_width() - base_w, x))
        y = max(80, min(screen.get_height() - base_h, y))
        return x, y

    # NEW: MOVABLE ORCA & ANIMATION ONLY WHEN MOVING
    def draw_orca(dest):
        nonlocal pos_x, pos_y, moving, last_frame_swap, use_glow
        dt = 1 / 30.0

        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        was_moving = moving  # NEW: track previous state for sound start/stop
        moving = (dx != 0 or dy != 0)

        # NEW: control sound playback based on movement state
        if orca_sound:
            if moving and not was_moving:
                try:
                    orca_sound.play(-1)  # NEW: loop while moving
                except Exception:
                    pass
            elif not moving and was_moving:
                try:
                    orca_sound.stop()     # NEW: stop when still
                except Exception:
                    pass

        if moving:
            if dx and dy:  # NEW: normalize diagonal speed
                dx *= 0.7071
                dy *= 0.7071
            pos_x += dx * speed * dt
            pos_y += dy * speed * dt
            pos_x, pos_y = clamp(pos_x, pos_y)

            now = pygame.time.get_ticks()
            if now - last_frame_swap >= frame_ms:
                use_glow = not use_glow
                last_frame_swap = now
        else:
            use_glow = False  # NEW: no glow unless moving

        frame = orca1
        if use_glow and orca2:
            frame = orca2
        if frame:
            dest.blit(frame, (int(pos_x), int(pos_y)))

    # NEW: INSTALL BACKGROUND & OVERLAY FOR THIS SCENE ONLY
    prev_bg = gui.set_background(draw_full_map)
    prev_fg = gui.set_overlay(draw_orca)

    try:
        gui.display("Foam hisses over tide pools. Loowit surfaces, watching you.")
        gui.pause(10000)  # CHANGED: true 10-second scene duration
        return "dock"
    finally:
        # NEW: ensure sound is stopped when leaving the scene
        if orca_sound:
            try:
                orca_sound.stop()
            except Exception:
                pass
        gui.set_background(prev_bg)
        gui.set_overlay(prev_fg)
