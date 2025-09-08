import pygame, sys, os, random

pygame.init()
W, H = 960, 540
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Player Animation")
clock = pygame.time.Clock()

ASSET_DIR = "assets"
#make sure you have player.png & player2.png in an assets folder in teh same directory, you can rename images if needed

def load_image(name):
    path = os.path.join(ASSET_DIR, name)
    return pygame.image.load(path).convert_alpha()

def scale_to_height(img, target_h):
    w, h = img.get_size()
    s = target_h / float(h)
    return pygame.transform.smoothscale(img, (int(w*s), int(h*s)))


SKY_BLUE = (135, 206, 235)
BROWN    = (139, 69, 19)

# ---------- load & scale ----------
PLAYER_H = 460  # you may need to change this size if your drawing is big or small
player_frames = [
    scale_to_height(load_image("player.png"), PLAYER_H),   
    scale_to_height(load_image("player2.png"), PLAYER_H)
    #add more images here
]

player = player_frames[0].get_rect(center=(W*0.3, H*0.50))

# ---------- moving state ----------
moving = False  # automatic movement is off
frame_i = 0
frame_timer = 0
frame_duration = random.randint(40, 400)  # ms for first frame

# ---------- loop ----------
while True:
    dt = clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            moving = not moving

    # ----  animation ----
    if moving:
        frame_timer += dt
        if frame_timer >= frame_duration:
            # swap state
            frame_i = 1 - frame_i  # 0 → 1 → 0 → 1 …
            #frame_i = (frame_i + 1) % 3 # % 3 makes it loop 0 → 1 → 2 → back to 0 forever.
            frame_timer = 0
            # pick new random length (short = fast, long = pause)
            if frame_i == 0:  # position 1
                frame_duration = random.randint(100, 300)
            else:             # position 2
                frame_duration = random.randint(120, 450)
    else:
        frame_i = 0  # idle frame

    # ---- Draw ----
    screen.fill(SKY_BLUE)
    ground_h = 120
    pygame.draw.rect(screen, BROWN, (0, H-ground_h, W, ground_h))

    screen.blit(player_frames[frame_i], player)

    pygame.display.flip()
