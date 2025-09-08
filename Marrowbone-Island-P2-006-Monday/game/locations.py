# game/locations.py
# location functions now accept a player; no global player module access

# removed all "from game import player" references (no more global state)
# updated every locations.py function to accept player (and pass it to gui)
import pygame
from game import gui
from game.sprite_sasquatch import Sasquatch  # NEW: animated Sasquatch sprite (sasquatch1/2.png)

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

def boat_house(player):
    gui.display([
        "you step into the damp, creaking boat house.",
        "a glint catches your eye behind an overturned canoe."
    ], player)
    gui.pause(2500)

    if "sling shot" not in player.gifts:
        player.gifts.append("sling shot")
        gui.display("you found a makeshift sling shot tangled in rope \nand take it with you.", player)
        gui.pause(2500)
    else:
        gui.display("the boat house is quiet. you've already searched it.", player)
        gui.pause(2000)
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
    gui.display("\nyou enter the cave.", player)

    if "Sasquatch" not in player.npcs:
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()

        sprites = pygame.sprite.Group()
        # fit him nicely in window
        target_h = int(screen.get_height() * 0.7)
        sas = Sasquatch(
            x=screen.get_width() // 2,
            y=screen.get_height() // 2,
            target_height=target_h
        )
        sprites.add(sas)

        font = pygame.font.SysFont("arial", 20)
        label  = font.render("Sasquatch (use arrows to move)", True, (0, 0, 0))
        prompt = font.render("press enter to continue", True, (0, 0, 0))

        showing = True
        while showing:
            dt = clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); raise SystemExit
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    showing = False

            # NEW: arrow key movement
            keys = pygame.key.get_pressed()
            speed = 5
            if keys[pygame.K_LEFT]:
                sas.rect.x -= speed
            if keys[pygame.K_RIGHT]:
                sas.rect.x += speed
            if keys[pygame.K_UP]:
                sas.rect.y -= speed
            if keys[pygame.K_DOWN]:
                sas.rect.y += speed

            screen.fill((60, 80, 90))  # cave background
            sprites.update(dt)         # Sasquatch animates only when moving
            sprites.draw(screen)

            screen.blit(label,  (20, 20))
            screen.blit(prompt, (20, 50))
            pygame.display.flip()

        # after scene ends, grant gift
        player.npcs.append("Sasquatch")
        if "magnetism" not in player.gifts:
            player.gifts.append("magnetism")
        gui.display("you meet sasquatch, who grants you magnetism!", player)

    else:
        gui.display("sasquatch is here as before.", player)

    return None



# tide_pools takes both player & sprites, instead of creating its own
def tide_pools(player, sprites):
    # uses the game's shared sprite group (e.g., loowit) passed in
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    instruction = pygame.font.SysFont("arial", 20).render(
        "press arrow keys to move. press enter to leave.", True, (0, 0, 0)
    )

    showing = True
    while showing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                showing = False

        screen.fill((100, 200, 180))
        # NOTE: some sprites (like Sasquatch) accept dt; others ignore it.
        dt = clock.get_time()
        try:
            sprites.update(dt)
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
