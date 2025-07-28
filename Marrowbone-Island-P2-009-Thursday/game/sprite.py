import pygame
import os

class LocationSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image1 = pygame.Surface((50, 50))
        self.image1.fill((255, 0, 0))
        self.image2 = pygame.Surface((50, 50))
        self.image2.fill((200, 0, 0))
        self.image = self.image1
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_counter = 0

    def update(self):
        self.animation_counter += 1
        if self.animation_counter % 30 < 15:
            self.image = self.image1
        else:
            self.image = self.image2

class TextObject(pygame.sprite.Sprite):
    def __init__(self, text, x, y):
        super().__init__()
        font = pygame.font.SysFont("Arial", 24)
        self.image = font.render(text, True, (255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image1 = pygame.image.load(os.path.join("assets", "player-1.png")).convert_alpha()
        self.image2 = pygame.image.load(os.path.join("assets", "player-2.png")).convert_alpha()
        self.image1 = pygame.transform.scale(self.image1, (300, 340))
        self.image2 = pygame.transform.scale(self.image2, (300, 340))
        self.image = self.image1
        self.rect = self.image.get_rect(center=(x + 140, y))  # start offset slightly right
        self.speed = 2
        self.animation_counter = 0

    def update(self):
        keys = pygame.key.get_pressed()
        moving = keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]

        if moving:
            self.animation_counter += 1
            if self.animation_counter % 30 < 15:
                self.image = self.image1
            else:
                self.image = self.image2

            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed
