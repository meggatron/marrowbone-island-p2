import pygame, sys, os, random

pygame.init()
W, H = 960, 540
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Player Talking")
clock = pygame.time.Clock()

ASSET_DIR = "assets"

# ---------- Helpers ----------
def load_image(name):
    path = os.path.join(ASSET_DIR, name)
    return pygame.image.load(path).convert_alpha()

def scale_to_height(img, target_h):
    w, h = img.get_size()
    s = target_h / float(h)
    return pygame.transform.smoothscale(img, (int(w*s), int(h*s)))

# ---------- Colors ----------
SKY_BLUE = (135, 206, 235)
BROWN    = (139, 69, 19)
BLACK    = (0, 0, 0)
WHITE    = (255, 255, 255)

# ---------- Load & Scale ----------
PLAYER_H = 460
player_frames = [
    scale_to_height(load_image("player.png"),  PLAYER_H),
    scale_to_height(load_image("player2.png"), PLAYER_H)
]
player = player_frames[0].get_rect(center=(W*0.3, H*0.50))

# ---------- Audio ----------
voice = None
try:
    voice = pygame.mixer.Sound(os.path.join(ASSET_DIR, "voice.wav"))
    voice.set_volume(0.9)
except Exception as e:
    print(f"[audio] Could not load voice.wav: {e}")

def start_voice():
    if voice is not None:
        voice.play(loops=-1)

def stop_voice():
    if voice is not None:
        voice.stop()

# ---------- Talking State ----------
talking = False
frame_i = 0
frame_timer = 0
frame_duration = random.randint(40, 400)

# ---------- Font ----------
font = pygame.font.SysFont("Arial", 28, bold=True)
speech_lines = [
    "Hi I've just arrived",
    "at Marrowstone Island",
    "but I seem to have",
    "lost my backpack"
]

# ---------- Loop ----------
while True:
    dt = clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            if not talking:
                talking = True
                start_voice()
                frame_timer = 0
        if e.type == pygame.KEYUP and e.key == pygame.K_SPACE:
            if talking:
                talking = False
                stop_voice()

    # ---- Talking animation ----
    if talking:
        frame_timer += dt
        if frame_timer >= frame_duration:
            frame_i = 1 - frame_i
            frame_timer = 0
            if frame_i == 0:
                frame_duration = random.randint(100, 300)
            else:
                frame_duration = random.randint(120, 450)
    else:
        frame_i = 0

    # ---- Draw ----
    screen.fill(SKY_BLUE)
    ground_h = 120
    pygame.draw.rect(screen, BROWN, (0, H-ground_h, W, ground_h))

    screen.blit(player_frames[frame_i], player)

    # ---- Speech text ----
    if talking:
        text_x = player.right + 30
        text_y = player.top + 80
        for line in speech_lines:
            surf = font.render(line, True, BLACK)
            screen.blit(surf, (text_x, text_y))
            text_y += surf.get_height() + 5

    pygame.display.flip()
