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
    gui.pause(1500)

def main():
    intro()
    current_location = "dock"

    while True:
        location_func = locations.locations[current_location]
        result = location_func()

        if result == "end":
            break

        if current_location == "tide_pools":
            screen.fill((100, 200, 180))
            all_sprites.update()
            all_sprites.draw(screen)
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                        waiting = False

        location_lines = ["Possible locations to go:"]
        for loc in locations.locations:
            if loc != "end":
                location_lines.append(f" - {loc.replace('_', ' ').title()}")
        gui.display(location_lines)
        gui.pause(1500)

        next_location = gui.get_input("Where do you want to go next? ").lower().replace(" ", "_")

        if next_location in locations.locations and next_location != "end":
            current_location = next_location
        else:
            gui.display("Invalid location. Try again.")
            gui.pause(1500)

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
