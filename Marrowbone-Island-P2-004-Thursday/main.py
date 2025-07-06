import pygame
from game import locations, player, gui

pygame.init()
pygame.display.set_mode((800, 600))


def intro():
    player.player_name = gui.get_input("What is your name, adventurer? ")
    gui.display(f"Welcome, {player.player_name}! Your adventure begins now.")
    gui.pause(1500)


def main():
    intro()
    current_location = "dock"

    while True:
        location_func = locations.locations[current_location]
        result = location_func()  # call the location function

        if result == "end":
            break  # stop the game loop if the game ended

        # Show list of locations
        location_lines = ["Possible locations to go:"]
        for loc in locations.locations:
            if loc != "end":
                location_lines.append(f" - {loc.replace('_', ' ').title()}")
        gui.display(location_lines)
        gui.pause(1500)

        # Get user input
        next_location = gui.get_input("Where do you want to go next? ").lower().replace(" ", "_")

        if next_location in locations.locations and next_location != "end":
            current_location = next_location
        else:
            gui.display("Invalid location. Try again.")
            gui.pause(1500)

        # Show status summary
        info_lines = [
            f"Inventory: {', '.join(player.inventory) if player.inventory else 'None'}",
            f"NPCs Met: {', '.join(player.npcs) if player.npcs else 'None'}",
            f"Gifts: {', '.join(player.gifts) if player.gifts else 'None'}"
        ]
        gui.display(info_lines)
        gui.pause(1500)

    gui.display("Thanks for playing!")
    gui.pause(1500)


if __name__ == "__main__":
    main()
