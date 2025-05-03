#easter egg/side quest

import random
import time

weather = ["foggy", "rainy", "sunny"]
inventory = []

def intro():
    with open("intro.txt", "r") as f:
        for line in f:
            print(line.strip())
    name = input("What is your name, adventurer? > ")
    print(f"Welcome, {name}. Your quest begins now...")
    return name

def log_room(location):
    with open("log.txt", "a") as log:
        log.write(f"Entered {location}\n")

def dock():
    log_room("dock")
    print(f"\nYou are on a {random.choice(weather)} dock. Paths lead north to a trail, west to a boathouse, and east to some tidepools.")
    move = input("Where do you go? > ").lower()
    if move in ["go north", "north"]:
        return 'trail'
    elif move in ["go west", "west"]:
        return 'boathouse'
    elif move in ["go east", "east"]:
        return 'tidepools'
    else:
        print("Try 'north', 'west', or 'east'.")
        return 'dock'

def trail():
    log_room("trail")
    print("\nYou begin walking up the trail.")
    for step in range(1, 4):
        print(f"Step {step}...")
        time.sleep(0.5)
    print(f"You are on a {random.choice(weather)} trail. Paths lead west to a forest, north to a cliff, south back to the dock, or east into a dark tunnel.")
    move = input("Where do you go? > ").lower()
    if move in ["go west", "west"]:
        return 'forest'
    elif move in ["go north", "north"]:
        return 'cliff'
    elif move in ["go south", "south"]:
        return 'dock'
    elif move in ["go east", "east"]:
        return 'tunnel'
    else:
        print("Try 'west', 'north', 'south', or 'east'.")
        return 'trail'

def forest():
    log_room("forest")
    print(f"\nYou step into a {random.choice(weather)} forest. The trees are thick and mossy. You can go west into a grove or east back to the trail.")
    if "map" not in inventory:
        take = input("You find a crumpled old map. Take it? (yes/no) > ").lower()
        if take == "yes":
            inventory.append("map")
            print("You take the map and tuck it into your coat.")
        else:
            print("You leave the map in the tree hollow.")
    else:
        print("The forest is quiet. You've already taken the map.")
    move = input("Where do you go? > ").lower()
    if move in ["go west", "west"]:
        return 'grove'
    elif move in ["go east", "east"]:
        return 'trail'
    else:
        print("Try 'west' or 'east'.")
        return 'forest'

def cliff():
    global player_name
    log_room("cliff")
    print(f"\nYou reach the edge of a {random.choice(weather)} cliff. A strange chest is buried here.")
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

def boathouse():
    log_room("boathouse")
    print(f"\nYou enter a {random.choice(weather)} boathouse. The air smells like mildew and salt.")
    print("A broken canoe leans against the wall. In the corner, a warped door leads to a small room.")
    move = input("Do you go into the laundry room? (yes/no) > ").lower()
    if move == "yes":
        return 'laundry_room'
    else:
        print("You return to the dock.")
        return 'dock'

def laundry_room():
    log_room("laundry_room")
    print("\nYou open the warped door. Water seeps across the floor.")
    time.sleep(1)
    print("A giant shrimp—at least eight feet long—stands beside a washing machine, folding towels.")
    time.sleep(2)
    print("He turns to you, antennae twitching. 'Would you like a poem?' he asks.")
    time.sleep(1)
    choice = input("Do you give the shrimp three words? (yes/no) > ").lower()
    if choice == "yes":
        noun = input("Give the shrimp a noun > ")
        emotion = input("How do you feel today? > ")
        adjective = input("Describe the sea in one word > ")
        print("\nThe shrimp bows and recites:\n")
        time.sleep(1)
        print(f"{noun} in moonlight")
        time.sleep(1.5)
        print(f"{emotion} flows through the tidepool")
        time.sleep(1.5)
        print(f"The sea is {adjective}.")
        time.sleep(2)
    else:
        print("The shrimp nods solemnly and returns to his towels.")
        time.sleep(1)
    print("You leave the laundry room.")
    return 'boathouse'

def tidepools():
    log_room("tidepools")
    print("\nYou scramble over slippery rocks at the tidepools. Barnacles crunch underfoot.")
    if random.choice([True, False]):
        print("An orca surfaces nearby, stares at you silently, then vanishes beneath the waves.")
    else:
        print("Just sea stars, urchins, and silence.")
    print("You can return west to the dock.")
    move = input("Where do you go? > ").lower()
    if move in ["go west", "west"]:
        return 'dock'
    else:
        print("Try typing 'west'.")
        return 'tidepools'

def grove():
    log_room("grove")
    print("\nYou enter a quiet grove. Ferns blanket the ground.")
    if random.choice([True, False]):
        print("You see massive footprints in the mud... too big to be human. They vanish into the underbrush.")
    else:
        print("Birdsong. Breeze. Just you and the trees.")
    print("You can go east to return to the forest.")
    move = input("Where do you go? > ").lower()
    if move in ["go east", "east"]:
        return 'forest'
    else:
        print("Try typing 'east'.")
        return 'grove'

def tunnel():
    log_room("tunnel")
    print("\nYou duck into a dark tunnel carved into the hillside.")
    print("A troll blocks the way. He squints at you.")
    if random.choice([True, False]):
        print("He grunts and steps aside, vanishing into the shadows.")
    else:
        print("He growls. 'Find the old cedar.' he says. You back away slowly.")
    print("You can go west to return to the trail.")
    move = input("Where do you go? > ").lower()
    if move in ["go west", "west"]:
        return 'trail'
    else:
        print("Try typing 'west'.")
        return 'tunnel'

player_name = intro()
current_location = 'dock'

locations = {
    'dock': dock,
    'trail': trail,
    'forest': forest,
    'cliff': cliff,
    'boathouse': boathouse,
    'laundry_room': laundry_room,
    'tidepools': tidepools,
    'grove': grove,
    'tunnel': tunnel
}

while current_location != 'end':
    current_location = locations[current_location]()