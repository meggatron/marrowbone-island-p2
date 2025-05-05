#gui
#sorting
#slicing
# main.py
from gui import GuiHandler
from locations import locations
from player import intro
import pygame

def wait_for_exit(gui):
    gui.display("\nthanks for playing. press esc or close the window to exit.")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        gui._render()
        gui.clock.tick(30)
    pygame.quit()

def main():
    gui = GuiHandler()
    player_name = intro(gui)
    current_location = 'dock'

    while current_location != 'end':
        current_location = locations[current_location](gui, player_name)

    wait_for_exit(gui)

if __name__ == "__main__":
    main()
