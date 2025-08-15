import pygame
from game import locations, player, gui

pygame.init()
# CHANGED: keep a handle to the display surface so we can blit the mini-map.
screen = pygame.display.set_mode((800, 600))

# NEW: load, scale, and position the mini-map (slightly under 1/4 screen)
try:
    map_img = pygame.image.load("assets/map.jpg").convert_alpha()  # adjust path if needed
except FileNotFoundError:
    map_img = None  # NEW: fail gracefully if the asset isn't present
else:
    mw = int(screen.get_width() * 0.23)   # NEW: scale to ~23% of screen width/height
    mh = int(screen.get_height() * 0.23)
    map_img = pygame.transform.smoothscale(map_img, (mw, mh))  # NEW
    MAP_POS = (screen.get_width() - mw - 10, screen.get_height() - mh - 10)  # NEW
    MAP_RECT = pygame.Rect(MAP_POS[0], MAP_POS[1], mw, mh)  # NEW

# NEW: register an overlay drawer so the mini-map appears on EVERY GUI frame
def _draw_overlay(dest_surface):
    if not map_img:
        return
    # .blit() pastes one surface onto another at (x, y).
    dest_surface.blit(map_img, MAP_POS)  # NEW

gui.set_overlay(_draw_overlay)  # NEW: hook overlay into gui.present() pipeline
# (Optional) If you want to restore later, save the previous overlay:
# prev_overlay = gui.set_overlay(_draw_overlay)


# CHANGED: draw_minimap() is no longer needed because gui will draw the overlay
#           automatically on every frame via gui.present(). Keeping the function
#           for reference, but it is unused.
def draw_minimap():
    if not map_img:
        return
    # .blit() pastes one surface onto another at (x, y).
    screen.blit(map_img, MAP_POS)  # NEW (legacy path)
    pygame.display.update(MAP_RECT)  # NEW (legacy path)


def intro():
    player.player_name = gui.get_input("What is your name, adventurer? ")
    gui.display(f"Welcome, {player.player_name}! Your adventure begins now.")
    # CHANGED: overlay auto-drawn by gui; removed manual draw_minimap()
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
        # CHANGED: overlay auto-drawn by gui; removed manual draw_minimap()

        # Special handling for Backpack (return to same place)
        if next_location == "backpack":
            current_location = locations.backpack(current_location)
            # CHANGED: overlay auto-drawn by gui; removed manual draw_minimap()
            continue
        elif next_location in locations.locations:
            current_location = next_location
        else:
            gui.display("Invalid location. Try again.")
            # CHANGED: overlay auto-drawn by gui; removed manual draw_minimap()
            gui.pause(1500)

        # Show status summary once per loop
        info_lines = [
            f"Inventory: {', '.join(player.inventory) if player.inventory else 'None'}",
            f"NPCs Met: {', '.join(player.npcs) if player.npcs else 'None'}",
            f"Gifts: {', '.join(player.gifts) if player.gifts else 'None'}"
        ]
        gui.display(info_lines)
        # CHANGED: overlay auto-drawn by gui; removed manual draw_minimap()
        gui.pause(2000)

    gui.display("Thanks for playing!")
    # CHANGED: overlay auto-drawn by gui; removed manual draw_minimap()
    gui.pause(1500)


if __name__ == "__main__":
    main()
