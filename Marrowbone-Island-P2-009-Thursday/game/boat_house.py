# game/boat_house.py
import pygame
import os
import math
from . import gui  # reuse your gui module

def boat_house(player):
    gui.display([
        "you step into the damp, creaking boat house.",
        "a glint catches your eye behind an overturned canoe."
    ], player)
    gui.pause(500)

    # If already collected before, short message and leave.
    if "sling shot" in player.gifts:
        gui.display("the boat house is quiet. you've already searched it.", player)
        gui.pause(800)
        return None

    screen = pygame.display.get_surface()
    clock  = pygame.time.Clock()
    W, H   = screen.get_width(), screen.get_height()

    ASSET_DIR = "assets"

    # ---- helpers (local; mirrors your working snippet) ----
    def load_image(name):
        return pygame.image.load(os.path.join(ASSET_DIR, name)).convert_alpha()

    def scale_to_height(img, target_h):
        w, h = img.get_size()
        s = target_h / float(h)
        return pygame.transform.smoothscale(img, (int(w * s), int(h * s)))

    # hand anchors (pixels relative to each sprite's rect)
    SHRIMP_XOFF, SHRIMP_YOFF = -18, -6  # pull left/up from right edge
    PLAYER_XOFF, PLAYER_YOFF = -14, +4  # tuck closer to torso

    def right_hand_pos(body_rect):
        # Shrimp hand → pull the slingshot in toward the claw a bit
        return (body_rect.right - 18, body_rect.centery - 6)

    def player_hand_pos(body_rect):
        # Player hand → tuck slightly inside the arm
        return (body_rect.right - 14, body_rect.centery + 4)

    def quad_bezier(p0, p1, p2, t):
        u = 1 - t
        x = u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0]
        y = u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1]
        return (x, y)

    # ---- load art; fail gracefully if missing ----
    try:
        player_img    = scale_to_height(load_image("player.png"),    int(H*0.38))
        shrimp_img    = scale_to_height(load_image("shrimp.png"),    int(H*0.42))
        slingshot_img = scale_to_height(load_image("slingshot.png"), int(H*0.10))
    except Exception as e:
        gui.display(f"(couldn't load boathouse art: {e})", player)
        if "sling shot" not in player.gifts:
            player.gifts.append("sling shot")
        gui.display("congratulations, you now have a slingshot!", player)
        gui.pause(5000)
        return None

    # ---- positions ----
    player_r = player_img.get_rect(center=(int(W*0.22), int(H*0.62)))
    shrimp_r = shrimp_img.get_rect(center=(int(W*0.74), int(H*0.62)))
    sling_r  = slingshot_img.get_rect(center=right_hand_pos(shrimp_r))

    # ---- state (matches your prototype timing) ----
    slingshot_state   = "idle_at_shrimp"  # -> animating_to_player -> attached_to_player
    t                 = 0.0
    ANIM_SPEED        = 0.06
    p0 = p1 = p2      = (0, 0)

    FREE_WALK_TIME    = 5.0    # time after pickup before banner
    free_walk_elapsed = 0.0
    got_slingshot     = False

    show_congrats     = False
    congrats_elapsed  = 0.0
    CONGRATS_TIME     = 5.0

    # ---- visuals ----
    floor_y    = int(H*0.78)
    font_small = pygame.font.SysFont("arial", 18)
    font_big   = pygame.font.SysFont("arial", 36)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # seconds
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); raise SystemExit

        # movement allowed before pickup and during free-walk; frozen during banner
        keys = pygame.key.get_pressed()
        speed = 4 if not show_congrats else 0
        if keys[pygame.K_RIGHT]: player_r.x += speed
        if keys[pygame.K_LEFT]:  player_r.x -= speed
        if keys[pygame.K_DOWN]:  player_r.y += speed
        if keys[pygame.K_UP]:    player_r.y -= speed

        # ---- FSM ----
        if slingshot_state == "idle_at_shrimp":
            sling_r.center = right_hand_pos(shrimp_r)

            # trigger: collide → set up quad Bézier
            if player_r.colliderect(shrimp_r):
                p0 = right_hand_pos(shrimp_r)
                p2 = player_hand_pos(player_r)
                midx   = 0.5 * (p0[0] + p2[0])
                apex_y = min(player_r.top - 80, p0[1] - 120)  # nice upward arc
                p1 = (midx, apex_y)
                t = 0.0
                slingshot_state = "animating_to_player"

        elif slingshot_state == "animating_to_player":
            t = min(1.0, t + ANIM_SPEED)
            x, y = quad_bezier(p0, p1, p2, t)
            sling_r.center = (int(x), int(y))
            if t >= 1.0:
                slingshot_state = "attached_to_player"
                if "sling shot" not in player.gifts:
                    player.gifts.append("sling shot")
                got_slingshot = True
                free_walk_elapsed = 0.0  # start free-walk timer

        elif slingshot_state == "attached_to_player":
            sling_r.center = player_hand_pos(player_r)

        # ---- timers controlling post-award flow ----
        if got_slingshot and not show_congrats:
            free_walk_elapsed += dt
            if free_walk_elapsed >= FREE_WALK_TIME:
                show_congrats = True
                congrats_elapsed = 0.0

        # ---- draw ----
        screen.fill((120, 130, 135))  # dim boathouse ambient
        pygame.draw.rect(screen, (139, 108, 78), (0, floor_y, W, H - floor_y))
        # order: sling under/over hands is okay either way here
        screen.blit(slingshot_img, sling_r)
        screen.blit(player_img,    player_r)
        screen.blit(shrimp_img,    shrimp_r)

        if show_congrats:
            congrats_elapsed += dt
            pulse = 180 + int(60 * math.sin(congrats_elapsed * 6.28318))  # gentle glow
            msg = font_big.render("Congratulations, you now have a slingshot!", True, (20,20,20))
            shade = pygame.Surface((W, 80), pygame.SRCALPHA)
            shade.fill((255, 255, 255, 110))
            screen.blit(shade, (0, 20))
            msg.set_alpha(pulse)
            screen.blit(msg, (max(20, (W - msg.get_width()) // 2), 36))
            if congrats_elapsed >= CONGRATS_TIME:
                running = False
        else:
            # only show hint before the banner period
            hint = font_small.render("walk over to the shrimp to take the slingshot", True, (15,15,15))
            screen.blit(hint, (16, 16))

        pygame.display.flip()

    return None
