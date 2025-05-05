import random

weather = ["foggy", "rainy", "sunny"]
inventory = []

def dock(gui, player_name):
    gui.log_room("dock")
    gui.display(f"\nyou are on a {random.choice(weather)} dock. paths lead north to a trail.")
    move = gui.get_input("where do you go? > ").lower()
    if move in ["go north", "north"]:
        return 'trail'
    else:
        gui.display("try typing 'go north'.")
        return 'dock'

def trail(gui, player_name):
    gui.log_room("trail")
    gui.display("\nyou begin walking up the trail.")
    for step in range(1, 4):
        gui.display(f"step {step}...")

    gui.display(f"you are on a {random.choice(weather)} trail. paths lead west into a forest, north to a cliff, or south back to the dock.")
    move = gui.get_input("where do you go? > ").lower()
    if move in ["go west", "west"]:
        return 'forest'
    elif move in ["go north", "north"]:
        return 'cliff'
    elif move in ["go south", "south"]:
        return 'dock'
    else:
        gui.display("try 'west', 'north', or 'south'.")
        return 'trail'

def forest(gui, player_name):
    gui.log_room("forest")
    gui.display(f"\nyou step into a {random.choice(weather)} forest. the trees are thick and mossy.")
    if "map" not in inventory:
        take = gui.get_input("you find a crumpled old map. take it? (yes/no) > ").lower()
        if take == "yes":
            inventory.append("map")
            gui.display("you take the map and tuck it into your coat.")
        else:
            gui.display("you leave the map in the tree hollow.")
    else:
        gui.display("the forest is quiet. you've already taken the map.")

    gui.display("you can go east to return to the trail.")
    move = gui.get_input("where do you go? > ").lower()
    if move in ["go east", "east"]:
        return 'trail'
    else:
        gui.display("try typing 'east'.")
        return 'forest'

def cliff(gui, player_name):
    gui.log_room("cliff")
    gui.display(f"\nyou reach the edge of a {random.choice(weather)} cliff. a strange chest is buried here, half-covered in moss and time.")

    if "map" in inventory:
        gui.display("you study the map one last time. the x marks a hollow beneath the old cedar.")
        gui.display("digging carefully, your fingers strike metal.")
        gui.display("you pull free a rusted chest. inside: silver coins, carved stones, and a locket still warm to the touch.")
        gui.display(f"no one will believe what you’ve found here, {player_name}.")
        gui.display("but the island remembers.")
        gui.display(f"congratulations {player_name}, you win marrowbone island!")
        return 'end'
    else:
        gui.display("the chest is here... but without the map, its meaning is lost.")
        gui.display("you can go south to return to the trail.")
        move = gui.get_input("where do you go? > ").lower()
        if move in ["go south", "south"]:
            return 'trail'
        else:
            gui.display("try typing 'south'.")
            return 'cliff'

locations = {
    'dock': dock,
    'trail': trail,
    'forest': forest,
    'cliff': cliff
}
