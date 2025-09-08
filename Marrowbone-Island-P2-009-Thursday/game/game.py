# game/game.py
# game composes the pieces: it owns a player and a group of sprites, and passes them to helpers

import pygame
from game import locations, gui
from game.player import Player  # imported the Player class directly
from game.sprite import NPC

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("marrowbone island")

        # composition: game has-a player (no global module state)
        self.player = Player()  # changed self.player = player → self.player = Player()
        self.current_location = "dock"

        # generalized sprites in game.py: game owns a sprite.Group, loowit is the first added
        # composition: game has-a group of sprites
        self.all_sprites = pygame.sprite.Group()
        # loowit is just the first sprite added, more could be added later
        self.all_sprites.add(NPC(400, 300))

    def intro(self):
        # gui functions now take the player the game owns
        self.player.name = gui.get_input("what is your name, adventurer? ", self.player)
        gui.display(f"welcome, {self.player.name}! your adventure begins now.", self.player)
        gui.pause(2000)

    def run(self):
        self.intro()

        while True:
            # look up the location function by key
            loc_fn = locations.locations[self.current_location]

            # pass owned state into the location (no globals)
            if self.current_location == "tide_pools":
                result = loc_fn(self.player, self.all_sprites)  # needs sprites
            else:
                result = loc_fn(self.player)

            if result == "end":
                gui.display("thanks for playing!", self.player)
                gui.pause(2000)
                break

            gui.pause(2000)

            # build the prompt of available locations
            location_lines = [
                f" - {loc.replace('_', ' ').title()}"
                for loc in locations.locations if loc != "end"
            ]
            prompt = (
                "possible locations to go:\n"
                + "\n".join(location_lines)
                + "\n\nwhere do you want to go next?"
            )
            prompt = prompt.encode("ascii", "ignore").decode()

            # read and normalize the next choice
            next_location = gui.get_input(prompt, self.player).lower().replace(" ", "_")
            gui.pause(300)

            # update or warn
            if next_location in locations.locations and next_location != "end":
                self.current_location = next_location
            else:
                gui.display("invalid location. try again.", self.player)
                gui.pause(2000)
