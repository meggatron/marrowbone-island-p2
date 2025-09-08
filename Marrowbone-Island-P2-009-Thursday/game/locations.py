# game/locations.py
# location functions now accept a player; no global player module access

# removed all "from game import player" references (no more global state)
# updated every locations.py function to accept player (and pass it to gui)
import pygame
from game import gui
from game.sprite_sasquatch import Sasquatch  # NEW: animated Sasquatch sprite (sasquatch1/2.png)
from game.boat_house import boat_house
# optional helpers using the player instance
def show_inventory(player):
    if not player.inventory:
        gui.display("your backpack is empty.", player)
    else:
        gui.display("your inventory:", player)
        for item in sorted(player.inventory):
            gui.display(f" - {item}", player)

def search_inventory(player, item_name):
    return any(item.lower() == item_name.lower() for item in player.inventory)

def dock(player):
    gui.display("\nyou arrive at the dock.", player)
    if "string" not in player.inventory:
        player.inventory.append("string")
        gui.display("you find a sturdy string and add it to your inventory.", player)
    else:
        gui.display("you already have the string here.", player)
    return None




def forest_trail(player):
    gui.display("\nyou walk along the forest trail.", player)
    if "loop" not in player.inventory:
        player.inventory.append("loop")
        gui.display("you find a loop and add it to your inventory.", player)
    else:
        gui.display("you already have the loop.", player)
    return None

def cave(player):
    # (Don't call gui.display() here—avoid stamping UI background into this scene)

    screen = pygame.display.get_surface()
    clock  = pygame.time.Clock()
    W, H   = screen.get_width(), screen.get_height()

    # ---- background ----
    try:
        bg = pygame.image.load("assets/island.jpg").convert()
        bg = pygame.transform.scale(bg, (W, H))
    except Exception as e:
        print(f"[cave] could not load background: {e}")
        bg = None

    # ---- player sprite (convert_alpha keeps transparent edges crisp) ----
    try:
        p_img_raw = pygame.image.load("assets/player.png").convert_alpha()
        target_h = int(H * 0.55)
        s = target_h / max(1, p_img_raw.get_height())
        player_img = pygame.transform.smoothscale(
            p_img_raw, (int(p_img_raw.get_width() * s), int(target_h))
        )
    except Exception as e:
        print(f"[cave] could not load player.png: {e}")
        player_img = pygame.Surface((int(W*0.10), int(H*0.30)), pygame.SRCALPHA)
        player_img.fill((0,150,255,255))

    player_rect = player_img.get_rect()
    player_rect.bottom = H - 8
    player_rect.right  = int(W * 0.88)

    # ---- Sasquatch (stationary) ----
    sprites = pygame.sprite.Group()
    sas = Sasquatch(x=int(W * 0.38), y=int(H * 0.70), target_height=int(H * 0.65))
    sprites.add(sas)

    label = pygame.font.SysFont("arial", 20).render(
        "use arrow keys to walk to Sasquatch", True, (30, 25, 20)
    )

    # ---- loop ----
    FLASHING = False
    flash_elapsed = 0.0
    FLASH_TOTAL = 1.0         # seconds of bolt flashing
    FLASH_MS    = 100         # swap cadence during flash (ms)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit

        if not FLASHING:
            keys = pygame.key.get_pressed()
            speed = 5
            if keys[pygame.K_LEFT]:  player_rect.x -= speed
            if keys[pygame.K_RIGHT]: player_rect.x += speed
            if keys[pygame.K_UP]:    player_rect.y -= speed
            if keys[pygame.K_DOWN]:  player_rect.y += speed
            player_rect.clamp_ip(screen.get_rect())

            if player_rect.colliderect(sas.rect):
                FLASHING = True
                flash_elapsed = 0.0

        # ---- draw (clear → bg → sprites) ----
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill((60, 80, 90))  # fallback

        if FLASHING:
            flash_elapsed += dt
            # toggle idle/bolts frames
            if (int((flash_elapsed * 1000) // FLASH_MS) % 2) == 0:
                sas.image = sas.frames[1]  # bolts
            else:
                sas.image = sas.frames[0]  # idle

        sprites.draw(screen)
        screen.blit(player_img, player_rect)

        if not FLASHING:
            screen.blit(label, (20, 20))

        pygame.display.flip()

        if FLASHING and flash_elapsed >= FLASH_TOTAL:
            running = False

    # ---- grant and exit (now safe to use gui.display) ----
    if "Sasquatch" not in player.npcs:
        player.npcs.append("Sasquatch")
    if "magnetism" not in player.gifts:
        player.gifts.append("magnetism")
    gui.display("you meet sasquatch, who grants you magnetism!", player)
    return None


def tide_pools(player, sprites):
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    instruction = pygame.font.SysFont("arial", 20).render(
        "press arrow keys to move. press enter to leave.", True, (0, 0, 0)
    )

    # load and scale map background once
    try:
        bg = pygame.image.load("assets/beach.jpeg").convert()
        bg = pygame.transform.scale(bg, (screen.get_width(), screen.get_height()))
    except Exception as e:
        print(f"[tide_pools] could not load background: {e}")
        bg = None

    showing = True
    while showing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                showing = False

        # draw map if available, else fallback color
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill((100, 200, 180))

        dt = clock.get_time()
        try:
            sprites.update(dt)   # Loowit glow animation
        except TypeError:
            sprites.update()
        sprites.draw(screen)
        screen.blit(instruction, (10, 10))
        pygame.display.flip()
        clock.tick(30)

    if "Loowit" not in player.npcs:
        player.npcs.append("Loowit")
        player.gifts.append("underwater breathing")
    return "continue"

def shipwreck(player):
    gui.display("\nyou find a shipwreck.", player)
    if "Ghost Pirate" not in player.npcs:
        player.npcs.append("Ghost Pirate")
        player.gifts.append("lantern")
        gui.display("the ghost pirate appears and gives you a lantern!", player)
    else:
        gui.display("the ghost pirate is here as before.", player)
    return None

def deep_reef(player):
    gui.display("\nyou dive into the deep reef.", player)
    if "coin" not in player.inventory:
        player.inventory.append("coin")
        gui.display("you find a shiny coin and add it to your inventory.", player)
    else:
        gui.display("you already have the coin.", player)
    return None

def cliff_face(player):
    gui.display("\nyou reach the cliff face.", player)
    if "iron mold" not in player.inventory:
        player.inventory.append("iron mold")
        gui.display("you find the iron mold and add it to your inventory.", player)
    else:
        gui.display("you already have the iron mold.", player)
    return None

def x_marks_spot(player):
    gui.display("""
    you arrive at the wind-swept dunes. 
    a crooked palm leans over an x scratched into the sand.
    """, player)
    gui.pause(1500)

    required_keys = {"coin", "loop", "string", "iron mold"}
    missing = required_keys - set(player.inventory)

    if missing:
        gui.display([
            "you start digging with your hands, the sand gives way easily...",
            f"but something’s missing: {', '.join(missing)}.",
            "whatever’s down there won’t open without everything."
        ], player)
        gui.pause(2500)
        return "dock"

    gui.display("you dig fast, sand flying, heart racing.", player); gui.pause(1500)
    gui.display("your fingers scrape something hard: a flat, rusted lid.", player); gui.pause(1500)
    gui.display("in its center: four strange dents, \njust the shape of the objects you've carried.", player); gui.pause(2000)
    gui.display("you place them in one by one. with the last piece, the lid shudders...", player); gui.pause(2000)
    gui.display("sand slides away as the box creaks open, revealing...", player); gui.pause(1500)
    gui.display("an ancient machine! brass gears, coiled wire, and a faint humming. \npirate treasure? maybe.", player); gui.pause(3000)
    return "end"

# exported mapping
locations = {
    "dock": dock,
    "boat_house": boat_house,
    "forest_trail": forest_trail,
    "cave": cave,
    "tide_pools": tide_pools,
    "shipwreck": shipwreck,
    "deep_reef": deep_reef,
    "cliff_face": cliff_face,
    "x_marks_spot": x_marks_spot,
}
