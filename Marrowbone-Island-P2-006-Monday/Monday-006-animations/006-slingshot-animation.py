import pygame, sys, os

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Shrimp → Slingshot → Player")
clock = pygame.time.Clock()

ASSET_DIR = "assets"

# ---------------- Helpers ----------------
def load_image(name):
    path = os.path.join(ASSET_DIR, name)
    img = pygame.image.load(path).convert_alpha()
    return img

def scale_to_height(img, target_h):
    w, h = img.get_size()
    scale = target_h / float(h)
    return pygame.transform.smoothscale(img, (int(w * scale), int(h * scale)))

def anchor_point(rect, ax, ay):
    return (rect.left + ax * rect.width, rect.top + ay * rect.height)

def quad_bezier(p0, p1, p2, t):
    u = 1 - t
    return (
        u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0],
        u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1],
    )

# ---------------- Load & Scale ----------------
PLAYER_H  = 180
SHRIMP_H  = 200
SLING_H   = 48

player_img    = scale_to_height(load_image("player.png"), PLAYER_H)
shrimp_img    = scale_to_height(load_image("shrimp.png"), SHRIMP_H)
slingshot_img = scale_to_height(load_image("slingshot.png"), SLING_H)

# ---------------- Rects ----------------
player = player_img.get_rect(center=(140, 300))
shrimp = shrimp_img.get_rect(center=(460, 300))
slingshot = slingshot_img.get_rect()

# ---------------- Anchors ----------------
SHRIMP_HAND_ANCHOR = (0.80, 0.50)
PLAYER_HAND_ANCHOR = (0.78, 0.56)
SHRIMP_HAND_NUDGE  = (+6, 0)
PLAYER_HAND_NUDGE  = (+6, 0)

# ---------------- State ----------------
slingshot_state = "idle_at_shrimp"
t = 0.0
ANIM_SPEED = 0.06
p0 = p1 = p2 = (0, 0)

# ---------------- Loop ----------------
while True:
    dt = clock.tick(60)  # ms since last frame
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    # ---------- Player Movement ----------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]: player.x += 3
    if keys[pygame.K_LEFT]:  player.x -= 3
    if keys[pygame.K_DOWN]:  player.y += 3
    if keys[pygame.K_UP]:    player.y -= 3

    # ---------- Anchor Positions ----------
    shrimp_hand = anchor_point(shrimp, *SHRIMP_HAND_ANCHOR)
    shrimp_hand = (shrimp_hand[0] + SHRIMP_HAND_NUDGE[0],
                   shrimp_hand[1] + SHRIMP_HAND_NUDGE[1])

    player_hand = anchor_point(player, *PLAYER_HAND_ANCHOR)
    player_hand = (player_hand[0] + PLAYER_HAND_NUDGE[0],
                   player_hand[1] + PLAYER_HAND_NUDGE[1])

    # ---------- Slingshot Logic ----------
    if slingshot_state == "idle_at_shrimp":
        slingshot.center = (int(shrimp_hand[0]), int(shrimp_hand[1]))
        if player.colliderect(shrimp):
            p0 = shrimp_hand
            p2 = player_hand
            midx = (p0[0] + p2[0]) * 0.5
            apex_y = min(player.top - 80, p0[1] - 120)
            p1 = (midx, apex_y)
            t = 0.0
            slingshot_state = "animating_to_player"

    elif slingshot_state == "animating_to_player":
        t = min(1.0, t + ANIM_SPEED)
        x, y = quad_bezier(p0, p1, p2, t)
        slingshot.center = (int(x), int(y))
        if t >= 1.0:
            slingshot_state = "attached_to_player"
            pygame.display.set_caption("You got the Slingshot!")

    elif slingshot_state == "attached_to_player":
        slingshot.center = (int(player_hand[0]), int(player_hand[1]))

    # ---------- Draw ----------
    screen.fill((135, 206, 235))  # sky blue background
    ground_rect = pygame.Rect(0, 380, 640, 100)
    pygame.draw.rect(screen, (139, 69, 19), ground_rect)  # brown ground

    # Draw sprites (order matters!)
    screen.blit(slingshot_img, slingshot)
    screen.blit(player_img, player)
    screen.blit(shrimp_img, shrimp)

    pygame.display.flip()
