import pygame, sys, os, random

pygame.init()
W, H = 960, 540
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("talking player + weather toggle")
clock = pygame.time.Clock()

ASSET_DIR = "assets"

def load_image(name):
    # helper function to load an image from the assets folder
    return pygame.image.load(os.path.join(ASSET_DIR, name)).convert_alpha()

def scale_to_height(img, target_h):
    # keep the image’s aspect ratio but scale its height to target_h
    w, h = img.get_size()
    s = target_h / float(h)
    return pygame.transform.smoothscale(img, (int(w*s), int(h*s)))

# colors for background and ground
SKY_BLUE = (135, 206, 235)   # default sunny sky
SKY_GRAY = (170, 170, 170)   # cloudy sky
BROWN    = (139, 69, 19)     # ground

# load player frames (two images: mouth closed and mouth open)
# pressing space will toggle the talking animation
PLAYER_H = 460
player_frames = [
    scale_to_height(load_image("player.png"),  PLAYER_H),   # frame 0 = mouth closed
    scale_to_height(load_image("player2.png"), PLAYER_H)    # frame 1 = mouth open
]
player_rect = player_frames[0].get_rect(center=(W*0.30, H*0.55))

# load weather icons (two images: sun and cloud)
# pressing w will toggle between them, and also switch the sky color
WEATHER_H = 160
weather_frames = [
    scale_to_height(load_image("weather1.png"), WEATHER_H),  # sun
    scale_to_height(load_image("weather2.png"), WEATHER_H),  # cloud
]
weather_rect = weather_frames[0].get_rect()
weather_rect.topright = (W - 24, 24)  # position in top right corner

# game state variables
weather_i = 0          # 0 = sun, 1 = cloud
talking = False        # whether the player is currently talking
frame_i = 0            # current player frame index
frame_timer = 0        # time since last frame change
frame_duration = 250   # how long each frame lasts in ms (controls talking speed)

# main game loop
while True:
    dt = clock.tick(60)  # limit to 60 frames per second and measure time since last loop
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w:
                # toggle the weather and background
                weather_i = 1 - weather_i
            if e.key == pygame.K_SPACE:
                # toggle the talking animation on and off
                talking = not talking
                frame_i = 0
                frame_timer = 0

    # update talking animation
    if talking:
        frame_timer += dt
        if frame_timer >= frame_duration:
            # flip between mouth closed (0) and open (1)
            frame_i = 1 - frame_i
            frame_timer = 0
    else:
        frame_i = 0  # idle = mouth closed

    # draw background (sky color changes with weather)
    bg = SKY_BLUE if weather_i == 0 else SKY_GRAY
    screen.fill(bg)

    # draw the ground at the bottom of the screen
    ground_h = 120
    pygame.draw.rect(screen, BROWN, (0, H-ground_h, W, ground_h))

    # draw the player character (showing current mouth frame)
    screen.blit(player_frames[frame_i], player_rect)

    # draw the weather icon in the top right
    screen.blit(weather_frames[weather_i], weather_rect)

    pygame.display.flip()
