import pygame

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path="assets/orca.png"):
        super().__init__()
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading image at {image_path}: {e}")
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))  # red box as fallback

        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        # Placeholder for future animation or behavior
        pass
