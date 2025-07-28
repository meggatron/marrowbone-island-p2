import pygame
from game import player
from game import gui
from game.sprite import LocationSprite, TextObject
from game.sprite import LocationSprite, TextObject
import os

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        image_path = os.path.join("assets", "player-1.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        pass  # You can add movement or animation later


def interactive_location(name, resident, color, item_name=None, item_pos=(200, 300), gift=False, sprite_override=None):
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    # player_sprite = sprite_override(x=400, y=300) if sprite_override else LocationSprite(400, 300)
    # player_sprite = sprite_override(x=400, y=300) if sprite_override else LocationSprite(400, 300)
    from game.sprite import PlayerSprite

    player_sprite = sprite_override(x=400, y=300) if sprite_override else PlayerSprite(400, 300)

    all_sprites = pygame.sprite.Group(player_sprite)
    items = pygame.sprite.Group()

    if item_name:
        item_sprite = TextObject(item_name, *item_pos)
        all_sprites.add(item_sprite)
        items.add(item_sprite)

    font = pygame.font.SysFont("Arial", 24)
    location_label = font.render(name.replace("_", " ").title(), True, (255, 255, 255))
    resident_label = font.render(f"Resident: {resident if resident else 'None'}", True, (255, 255, 255))

    showing = True
    while showing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill(color)
        all_sprites.update()
        all_sprites.draw(screen)
        screen.blit(location_label, (10, 10))
        screen.blit(resident_label, (600, 10))

        if item_name and pygame.sprite.spritecollide(player_sprite, items, dokill=True):
            if gift:
                player.gifts.append(item_name)
            else:
                player.inventory.append(item_name)
            showing = False

        pygame.display.flip()
        clock.tick(30)

    if resident and resident not in player.npcs:
        player.npcs.append(resident)

    return "continue"

def dock():
    return interactive_location("dock", None, (20, 80, 160), item_name="string")

def boat_house():
    return interactive_location("boat_house", "Shrimp", (60, 60, 100), item_name="sling shot", gift=True)

def forest_trail():
    return interactive_location("forest_trail", "None", (50, 120, 50), item_name="loop")

def cave():
    return interactive_location("cave", "Sasquatch", (80, 50, 80), item_name="magnetism", gift=True)

def tide_pools():
    return interactive_location("tide_pools", "Loowit", (100, 200, 180), item_name="underwater breathing", gift=True)

def shipwreck():
    return interactive_location("shipwreck", "Ghost Pirate", (70, 70, 150), item_name="lantern", gift=True)

def deep_reef():
    return interactive_location("deep_reef", "None", (30, 50, 100), item_name="coin")

def cliff_face():
    return interactive_location("cliff_face", "None", (90, 90, 90), item_name="iron mold")

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
