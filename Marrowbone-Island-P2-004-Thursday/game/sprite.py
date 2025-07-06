import pygame

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path="assets/orca.png"):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))