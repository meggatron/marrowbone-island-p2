import random
import time

weather = ["foggy", "rainy", "sunny"]
inventory = []

def log_room(location):
    with open("log.txt", "a") as log:
        log.write(f"Entered {location}\n")

def dock(player_name):
    log_room("dock")
    print(f"\nYou are on a {random.choice(weather)} dock. Paths lead north to a trail.")
    move = input("Where do you go? > ").lower()
    if move in ["go north", "north"]:
        return 'trail'
    else:
        print("Try typing 'go north'.")
        return 'dock'

def trail(player_name):
    log_room("trail")
    print("\nYou begin walking up the trail.")
    for step in range(1, 4):
        print(f"Step {step}...")
        time.sleep(0.5)
    print(f"You are on a {random.choice(weather)} trail. Paths lead west into a forest, north to a cliff, or south back to the dock.")
    move = input("Where do you go? > ").lower()
    if move in ["go west", "west"]:
        return 'forest'
    elif move in ["go north", "north"]:
        return 'cliff'
    elif move in ["go south", "south"]:
        return 'dock'
    else:
        print("Try 'west', 'north', or 'south'.")
        return 'trail'

def forest(player_name):
    log_room("forest")
    print(f"\nYou step into a {random.choice(weather)} forest. The trees are thick and mossy.")
    if "map" not in inventory:
        take = input("You find a crumpled old map. Take it? (yes/no) > ").lower()
        if take == "yes":
            inventory.append("map")
            print("You take the map and tuck it into your coat.")
        else:
            print("You leave the map in the tree hollow.")
    else:
        print("The forest is quiet. You've already taken the map.")
    print("You can go east to return to the trail.")
    move = input("Where do you go? > ").lower()
    if move in ["go east", "east"]:
        return 'trail'
    else:
        print("Try typing 'east'.")
        return 'forest'

def cliff(player_name):
    log_room("cliff")
    print(f"\nYou reach the edge of a {random.choice(weather)} cliff. A strange chest is buried here, half-covered in moss and time.")
    if "map" in inventory:
        time.sleep(1)
        print("You study the map one last time. The X marks a hollow beneath the old cedar.")
        time.sleep(2)
        print("Digging carefully, your fingers strike metal.")
        time.sleep(2)
        print("You pull free a rusted chest. Inside: silver coins, carved stones, and a locket still warm to the touch.")
        time.sleep(3)
        print(f"No one will believe what you’ve found here, {player_name}.")
        time.sleep(2)
        print("But the island remembers.")
        time.sleep(2)
        print(f"Congratulations {player_name}, you win Marrowbone Island!")
        return 'end'
    else:
        print("The chest is here... but without the map, its meaning is lost.")
        print("You can go south to return to the trail.")
        move = input("Where do you go? > ").lower()
        if move in ["go south", "south"]:
            return 'trail'
        else:
            print("Try typing 'south'.")
            return 'cliff'

locations = {
    'dock': dock,
    'trail': trail,
    'forest': forest,
    'cliff': cliff
}
