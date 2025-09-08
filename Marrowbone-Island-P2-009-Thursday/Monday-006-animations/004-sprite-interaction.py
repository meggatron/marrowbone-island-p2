import pygame, sys

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
pygame.display.set_caption("Sprite Interaction")

# ----------- Helpers ------------
def right_hand_pos(body_rect):
    """Return a point at the right 'hand' (right edge, mid-height)."""
    return (body_rect.right + 8, body_rect.centery)

def player_hand_pos(body_rect):
    """Where the slingshot should sit on the player when attached."""
    return (body_rect.right + 8, body_rect.centery)

def quad_bezier(p0, p1, p2, t):
    """Quadratic Bézier interpolation."""
    u = 1 - t
    x = u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0]
    y = u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1]
    return (x, y)

# ----------- Sprites are created ------------
# Player & Shrimp as tall rounded rectangles
player_img = pygame.Surface((30, 90), pygame.SRCALPHA)
pygame.draw.rect(player_img, (0, 150, 255), player_img.get_rect(), border_radius=6)

shrimp_img = pygame.Surface((30, 90), pygame.SRCALPHA)
pygame.draw.rect(shrimp_img, (255, 120, 40), shrimp_img.get_rect(), border_radius=6)

# Slingshot as white circle with transparent background
SLING_R = 10
slingshot_img = pygame.Surface((SLING_R*2+4, SLING_R*2+4), pygame.SRCALPHA)
pygame.draw.circle(slingshot_img, (255, 255, 255), (SLING_R+2, SLING_R+2), SLING_R)

# Sprite Rects
player = player_img.get_rect(center=(120, 240))
shrimp = shrimp_img.get_rect(center=(420, 240))
slingshot = slingshot_img.get_rect(center=right_hand_pos(shrimp))

# ----------- Idle state ------------
slingshot_state = "idle_at_shrimp"   # idle_at_shrimp -> animating_to_player -> attached_to_player
t = 0.0
ANIM_SPEED = 0.06
p0 = p1 = p2 = (0, 0)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]: player.x += 3
    if keys[pygame.K_LEFT]:  player.x -= 3
    if keys[pygame.K_DOWN]:  player.y += 3
    if keys[pygame.K_UP]:    player.y -= 3

    # ----------- Idle state ------------
    if slingshot_state == "idle_at_shrimp":
        slingshot.center = right_hand_pos(shrimp)

        # ----------- Trigger ------------
        if player.colliderect(shrimp):
            p0 = right_hand_pos(shrimp)
            p2 = player_hand_pos(player)
            midx = (p0[0] + p2[0]) * 0.5
            apex_y = min(player.top - 80, p0[1] - 120)
            p1 = (midx, apex_y)
            t = 0.0
            slingshot_state = "animating_to_player"

    # ----------- Animation ------------
    elif slingshot_state == "animating_to_player":
        t = min(1.0, t + ANIM_SPEED)
        x, y = quad_bezier(p0, p1, p2, t)
        slingshot.center = (int(x), int(y))

        if t >= 1.0:
            slingshot_state = "attached_to_player"
            print("You got the slingshot!")

    # ----------- Attached state ------------
    elif slingshot_state == "attached_to_player":
        slingshot.center = player_hand_pos(player)

    # ----------- Draw loop ------------
    screen.fill((30, 30, 30))
    screen.blit(shrimp_img, shrimp)
    screen.blit(slingshot_img, slingshot)
    screen.blit(player_img, player)



    pygame.display.flip()
    clock.tick(60)
