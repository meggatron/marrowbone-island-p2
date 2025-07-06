from game import player

def backpack():
    while True:
        print("\nYou open your backpack. What would you like to do?")
        print("1. View sorted inventory")
        print("2. Search for an item")
        print("3. Close backpack")

        choice = input("> ").strip()

        if choice == "1":
            show_inventory(player.inventory)
        elif choice == "2":
            item = input("What item are you looking for? ").strip()
            if search_inventory(player.inventory, item):
                print(f"You have the {item}.")
            else:
                print(f"The {item} isn’t here.")
        elif choice == "3":
            print("You close your backpack.")
            return "dock"  # or return to previous location
        else:
            print("The backpack rustles... but offers no answer.")

def show_inventory(inventory):
    if not inventory:
        print("Your backpack is empty.")
    else:
        print("Your inventory:")
        for item in sorted(inventory):
            print(f" - {item}")

def search_inventory(inventory, item_name):
    for item in inventory:
        if item.lower() == item_name.lower():
            return True
    return False


def dock():
    print("\nYou arrive at the Dock.")
    if "string" not in player.inventory:
        player.inventory.append("string")
        print("You find a sturdy string and add it to your inventory.")
    else:
        print("You already have the string here.")

def boat_house():
    print("\nYou enter the Boat House.")
    if "Giant Shrimp" not in player.npcs:
        player.npcs.append("Giant Shrimp")
        player.gifts.append("sling shot")
        print("The Giant Shrimp greets you and grants you a sling shot!")
    else:
        print("The Giant Shrimp is here as before.")

def forest_trail():
    print("\nYou walk along the Forest Trail.")
    if "loop" not in player.inventory:
        player.inventory.append("loop")
        print("You find a loop and add it to your inventory.")
    else:
        print("You already have the loop.")

def cave():
    print("\nYou enter the Cave.")
    if "Sasquatch" not in player.npcs:
        player.npcs.append("Sasquatch")
        player.gifts.append("magnetism")
        print("You meet Sasquatch, who grants you magnetism!")
    else:
        print("Sasquatch is here as before.")

def tide_pools():
    print("\nYou reach the Tide Pools.")
    if "Loowit" not in player.npcs:
        player.npcs.append("Loowit")
        player.gifts.append("underwater breathing")
        print("You meet Loowit, the orca, who grants you underwater breathing!")
    else:
        print("Loowit is here as before.")

def shipwreck():
    print("\nYou find a Shipwreck.")
    if "Ghost Pirate" not in player.npcs:
        player.npcs.append("Ghost Pirate")
        player.gifts.append("lantern")
        print("The Ghost Pirate appears and gives you a lantern!")
    else:
        print("The Ghost Pirate is here as before.")

def deep_reef():
    print("\nYou dive into the Deep Reef.")
    if "coin" not in player.inventory:
        player.inventory.append("coin")
        print("You find a shiny coin and add it to your inventory.")
    else:
        print("You already have the coin.")

def cliff_face():
    print("\nYou reach the Cliff Face.")
    if "iron mold" not in player.inventory:
        player.inventory.append("iron mold")
        print("You find the iron mold and add it to your inventory.")
    else:
        print("You already have the iron mold.")

def x_marks_spot():
    print("\nYou arrive at X Marks the Spot — the final location!")
    required_items = ["string", "loop", "coin", "iron mold"]
    required_gifts = ["sling shot", "magnetism", "underwater breathing", "lantern"]

    if all(item in player.inventory for item in required_items) and all(gift in player.gifts for gift in required_gifts):
        print("You have all the items and powers needed to unlock the treasure!")
        print(f"Congratulations, {player.player_name}, you win Marrowbone Island!")
        return "end"
    else:
        print("You don't have everything you need yet. Keep exploring!")
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
