import pygame

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [
            pygame.image.load("assets/orca.png").convert_alpha(),
            pygame.image.load("assets/orca-glow.png").convert_alpha()
        ]
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.counter = 0
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT]:
            dx = -5
        if keys[pygame.K_RIGHT]:
            dx = 5
        if keys[pygame.K_UP]:
            dy = -5
        if keys[pygame.K_DOWN]:
            dy = 5

        # Move the sprite
        self.rect.x += dx
        self.rect.y += dy

        # Animate only if moving
        if dx != 0 or dy != 0:
            self.counter += 1
            if self.counter % 15 == 0:
                self.current_image = (self.current_image + 1) % len(self.images)
                self.image = self.images[self.current_image]
        else:
            # Stay on the default image when not moving
            self.current_image = 0
            self.image = self.images[self.current_image]
