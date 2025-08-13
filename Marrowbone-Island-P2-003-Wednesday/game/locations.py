from game import player
import random, time

weather = ["foggy", "rainy", "sunny"]


def dock(player_name):
    print(f"\nYou are on a {random.choice(weather)} dock. A small boathouse sits nearby. Paths lead north to a trail or east to the boathouse.")

    if "string" not in player.backpack.items:
        take = input("You find a coil of string. Take it? (yes/no, or 'backpack') > ").lower()
        if take in ["backpack", "open backpack"]:
            player.backpack.menu()
            return 'dock'
        if take == "yes":
            player.backpack.add_item("string")
            print("You take the string and tuck it into your coat.")
        else:
            print("You leave the string where it is.")

    move = input("Where do you go? (north/east, or 'backpack') > ").lower()
    if move in ["backpack", "open backpack"]:
        player.backpack.menu()
        return 'dock'
    if move in ["go north", "north"]:
        return 'trail'
    if move in ["go east", "east"]:
        return 'boathouse'
    print("Try typing 'north' or 'east'.")
    return 'dock'

def boathouse(player_name):
    print(f"\nYou enter the boathouse. It smells of salt and old wood.")
    print("A giant shrimp is here, humming to itself.")
    move = input("Where do you go? (west to dock, or 'backpack') > ").lower()
    if move in ["backpack", "open backpack"]:
        player.backpack.menu()
        return 'boathouse'
    if move in ["go west", "west"]:
        return 'dock'
    print("Try typing 'west'.")
    return 'boathouse'

def trail(player_name):
    print("\nYou begin walking up the trail.")
    for step in range(1, 4):
        print(f"Step {step}...")
        time.sleep(0.5)
    print(f"You are on a {random.choice(weather)} trail. Paths lead west into a forest, north to a cliff, or south back to the dock.")
    move = input("Where do you go? (tip: 'backpack') > ").lower()
    if move in ["backpack", "open backpack"]:
        player.backpack.menu()
        return 'trail'
    if move in ["go west", "west"]:
        return 'forest'
    if move in ["go north", "north"]:
        return 'cliff'
    if move in ["go south", "south"]:
        return 'dock'
    print("Try 'west', 'north', or 'south'.")
    return 'trail'

def forest(player_name):
    print(f"\nYou step into a {random.choice(weather)} forest. The trees are thick and mossy.")
    if "map" not in player.backpack.items:
        take = input("You find a crumpled old map. Take it? (yes/no, or 'backpack') > ").lower()
        if take in ["backpack", "open backpack"]:
            player.backpack.menu()
            return 'forest'
        if take == "yes":
            player.backpack.add_item("map")
            print("You take the map and tuck it into your coat.")
        else:
            print("You leave the map in the tree hollow.")
    else:
        print("The forest is quiet. You've already taken the map.")
    print("You can go east to return to the trail.")
    move = input("Where do you go? (tip: 'backpack') > ").lower()
    if move in ["backpack", "open backpack"]:
        player.backpack.menu()
        return 'forest'
    if move in ["go east", "east"]:
        return 'trail'
    print("Try typing 'east'.")
    return 'forest'

def cliff(player_name):
    print(f"\nYou reach the edge of a {random.choice(weather)} cliff. A strange chest is buried here, half-covered in moss and time.")
    if "map" in player.backpack.items:
        time.sleep(1); print("You study the map one last time. The X marks a hollow beneath the old cedar.")
        time.sleep(2); print("Digging carefully, your fingers strike metal.")
        time.sleep(2); print("You pull free a rusted chest. Inside: silver coins, carved stones, and a locket still warm to the touch.")
        time.sleep(3); print(f"No one will believe what you’ve found here, {player_name}.")
        time.sleep(2); print("But the island remembers.")
        time.sleep(2); print(f"Congratulations {player_name}, you win Marrowbone Island!")
        return 'end'
    else:
        print("The chest is here... but without the map, its meaning is lost.")
        print("You can go south to return to the trail.")
        move = input("Where do you go? (tip: 'backpack') > ").lower()
        if move in ["backpack", "open backpack"]:
            player.backpack.menu()
            return 'cliff'
        if move in ["go south", "south"]:
            return 'trail'
        print("Try typing 'south'.")
        return 'cliff'

locations = {
    'dock': dock,
    'boathouse': boathouse,
    'trail': trail,
    'forest': forest,
    'cliff': cliff
}
