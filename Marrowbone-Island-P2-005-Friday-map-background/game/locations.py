import pygame
from game import player
from game import gui
from game.sprite import NPC
from game.tide_pools import tide_pools

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
    return None



def boat_house():
    gui.display([
        "You step into the damp, creaking Boat House.",
        "A glint catches your eye behind an overturned canoe."
    ])
    gui.pause(2500)

    if "sling shot" not in player.gifts:
        player.gifts.append("sling shot")
        gui.display("You found a makeshift sling shot tangled in rope \nand take it with you.")
        gui.pause(2500)
    else:
        gui.display("The boat house is quiet. You've already searched it.")
        gui.pause(2000)

    return None

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
    gui.display("""
    You arrive at the wind-swept dunes. 
    A crooked palm leans over an X scratched into the sand.
    """)

    gui.pause(1500)

    required_keys = {"coin", "loop", "string", "iron mold"}
    missing = required_keys - set(player.inventory)

    if missing:
        gui.display([
            "You start digging with your hands, the sand gives way easily...",
            f"But something’s missing: {', '.join(missing)}.",
            "Whatever’s down there won’t open without everything."
        ])
        gui.pause(2500)
        return "dock"

    gui.display("You dig fast, sand flying, heart racing.")
    gui.pause(1500)
    gui.display("Your fingers scrape something hard: a flat, rusted lid.")
    gui.pause(1500)
    gui.display("In its center: four strange dents, \njust the shape of the objects you've carried.")
    gui.pause(2000)
    gui.display("You place them in one by one. With the last piece, the lid shudders...")
    gui.pause(2000)
    gui.display("Sand slides away as the box creaks open, revealing...")
    gui.pause(1500)
    gui.display("An ancient machine! Brass gears, coiled wire, and a faint humming. \nPirate treasure? Maybe.")
    gui.pause(3000)
    return "end"


locations = {
    "dock": dock,
    "boat_house": boat_house,
    "forest_trail": forest_trail,
    "cave": cave,
    "tide_pools": tide_pools,
    "shipwreck": shipwreck,
    "deep_reef": deep_reef,
    "cliff_face": cliff_face,
    "x_marks_spot": x_marks_spot
}
