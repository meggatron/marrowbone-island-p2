import pygame
from game import player
from game import gui
from game.sprite import NPC

def backpack():
    while True:
        gui.display("\nYou open your backpack. What would you like to do?")
        gui.display("1. View sorted inventory")
        gui.display("2. Search for an item")
        gui.display("3. Close backpack")
        gui.pause(1500)

        choice = gui.get_input("> ").strip()

        if choice == "1":
            show_inventory(player.inventory)
            gui.pause(1500)
        elif choice == "2":
            item = gui.get_input("What item are you looking for? ").strip()
            if search_inventory(player.inventory, item):
                gui.display(f"You have the {item}.")
                gui.pause(1500)
            else:
                gui.display(f"The {item} isn’t here.")
                gui.pause(1500)
        elif choice == "3":
            gui.display("You close your backpack.")
            gui.pause(1500)
            return "dock"
        else:
            gui.display("The backpack rustles... but offers no answer.")

def show_inventory(inventory):
    if not inventory:
        gui.display("Your backpack is empty.")
    else:
        gui.display("Your inventory:")
        for item in sorted(inventory):
            gui.display(f" - {item}")

def search_inventory(inventory, item_name):
    for item in inventory:
        if item.lower() == item_name.lower():
            return True
    return False


def dock():
    gui.display("\nYou arrive at the Dock.")
    if "string" not in player.inventory:
        player.inventory.append("string")
        gui.display("You find a sturdy string and add it to your inventory.")
    else:
        gui.display("You already have the string here.")

def boat_house():
    gui.display("\nYou enter the Boat House.")
    gui.get_input("[Press Enter to continue]")
    if "Giant Shrimp" not in player.npcs:
        player.npcs.append("Giant Shrimp")
        player.gifts.append("sling shot")
        gui.display("The Giant Shrimp greets you and grants you a sling shot!")
    else:
        gui.display("The Giant Shrimp is here as before.")

def forest_trail():
    gui.display("\nYou walk along the Forest Trail.")
    if "loop" not in player.inventory:
        player.inventory.append("loop")
        gui.display("You find a loop and add it to your inventory.")
    else:
        gui.display("You already have the loop.")

def cave():
    gui.display("\nYou enter the Cave.")
    if "Sasquatch" not in player.npcs:
        player.npcs.append("Sasquatch")
        player.gifts.append("magnetism")
        gui.display("You meet Sasquatch, who grants you magnetism!")
    else:
        gui.display("Sasquatch is here as before.")

def tide_pools():
    import pygame
    from game.sprite import NPC

    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    loowit = NPC(400, 300)
    all_sprites = pygame.sprite.Group(loowit)

    showing = True
    while showing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # press Enter to continue
                    showing = False

        screen.fill((100, 200, 180))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    return "continue"


def shipwreck():
    gui.display("\nYou find a Shipwreck.")
    if "Ghost Pirate" not in player.npcs:
        player.npcs.append("Ghost Pirate")
        player.gifts.append("lantern")
        gui.display("The Ghost Pirate appears and gives you a lantern!")
    else:
        gui.display("The Ghost Pirate is here as before.")

def deep_reef():
    gui.display("\nYou dive into the Deep Reef.")
    if "coin" not in player.inventory:
        player.inventory.append("coin")
        gui.display("You find a shiny coin and add it to your inventory.")
    else:
        gui.display("You already have the coin.")

def cliff_face():
    gui.display("\nYou reach the Cliff Face.")
    if "iron mold" not in player.inventory:
        player.inventory.append("iron mold")
        gui.display("You find the iron mold and add it to your inventory.")
    else:
        gui.display("You already have the iron mold.")

def x_marks_spot():
    gui.display("\nYou arrive at X Marks the Spot — the final location!")
    required_items = ["string", "loop", "coin", "iron mold"]
    required_gifts = ["sling shot", "magnetism", "underwater breathing", "lantern"]

    if all(item in player.inventory for item in required_items) and all(gift in player.gifts for gift in required_gifts):
        gui.display("You have all the items and powers needed to unlock the treasure!")
        gui.display(f"Congratulations, {player.player_name}, you win Marrowbone Island!")
        return "end"
    else:
        gui.display("You don't have everything you need yet. Keep exploring!")
        # No return means the game continues


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
    "backpack": backpack
    }
