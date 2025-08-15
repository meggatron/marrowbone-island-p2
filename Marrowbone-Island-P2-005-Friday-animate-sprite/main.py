import pygame
from game import locations, player, gui
from game.sprite import NPC

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Marrowbone Island")

loowit = NPC(400, 300)
all_sprites = pygame.sprite.Group(loowit)

def intro():
    player.player_name = gui.get_input("What is your name, adventurer? ")
    gui.display(f"Welcome, {player.player_name}! Your adventure begins now.")
    gui.pause(2000)

def main():
    intro()
    current_location = "dock"

    while True:
        location_func = locations.locations[current_location]
        result = location_func()

        if result == "end":
            gui.display("Thanks for playing!")
            gui.pause(2000)
            break

        gui.pause(2000)

        location_lines = [
            f" - {loc.replace('_', ' ').title()}"
            for loc in locations.locations if loc != "end"
        ]
        prompt = (
            "Possible locations to go:\n" +
            "\n".join(location_lines) +
            "\n\nWhere do you want to go next?"
        )
        prompt = prompt.encode("ascii", "ignore").decode()

        next_location = gui.get_input(prompt).lower().replace(" ", "_")
        gui.pause(300)

        if next_location in locations.locations and next_location != "end":
            current_location = next_location
        else:
            gui.display("Invalid location. Try again.")
            gui.pause(2000)

if __name__ == "__main__":
    print("Starting the game...")
    main()
