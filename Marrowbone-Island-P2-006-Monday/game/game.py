import pygame
from game import locations, player, gui
from game.sprite import NPC

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Marrowbone Island")

        self.player = player
        self.locations = locations.locations
        self.current_location = "dock"

        # Sprite setup
        self.loowit = NPC(400, 300)
        self.all_sprites = pygame.sprite.Group(self.loowit)

    def intro(self):
        self.player.player_name = gui.get_input("What is your name, adventurer? ")
        gui.display(f"Welcome, {self.player.player_name}! Your adventure begins now.")
        gui.pause(2000)

    def run(self):
        self.intro()

        while True:
            location_func = self.locations[self.current_location]
            result = location_func()

            if result == "end":
                gui.display("Thanks for playing!")
                gui.pause(2000)
                break

            gui.pause(2000)

            location_lines = [
                f" - {loc.replace('_', ' ').title()}"
                for loc in self.locations if loc != "end"
            ]
            prompt = (
                "Possible locations to go:\n" +
                "\n".join(location_lines) +
                "\n\nWhere do you want to go next?"
            )
            prompt = prompt.encode("ascii", "ignore").decode()

            next_location = gui.get_input(prompt).lower().replace(" ", "_")
            gui.pause(300)

            if next_location in self.locations and next_location != "end":
                self.current_location = next_location
            else:
                gui.display("Invalid location. Try again.")
                gui.pause(2000)
