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
            break

        # Build location list prompt (add Backpack manually)
        location_list = [
            f" - {loc.replace('_', ' ').title()}"
            for loc in locations.locations
        ]
        prompt = (
            "Possible locations to go:\n"
            + "\n".join(location_list)
            + "\n - Backpack"
            + "\n\nWhere do you want to go next?"
        )

        # Strip non-ASCII characters just in case
        prompt = prompt.encode("ascii", "ignore").decode()

        next_location = gui.get_input(prompt).lower().strip().replace(" ", "_")

        # Special handling for Backpack (return to same place)
        if next_location == "backpack":
            current_location = locations.backpack(current_location)
            continue
        elif next_location in locations.locations:
            current_location = next_location
        else:
            gui.display("Invalid location. Try again.")
            gui.pause(1500)

        # Show status summary once per loop
        info_lines = [
            f"Inventory: {', '.join(player.inventory) if player.inventory else 'None'}",
            f"NPCs Met: {', '.join(player.npcs) if player.npcs else 'None'}",
            f"Gifts: {', '.join(player.gifts) if player.gifts else 'None'}"
        ]
        gui.display(info_lines)
        gui.pause(2000)

    gui.display("Thanks for playing!")
    gui.pause(1500)


if __name__ == "__main__":
    main()
