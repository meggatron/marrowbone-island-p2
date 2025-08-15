import pygame


class NPC(pygame.sprite.Sprite):
    """
    2-frame sprite that ONLY animates while moving.
    - Frames: assets/orca.png, assets/orca-glow.png
    """
    def __init__(self, x: int, y: int,
                 frame_paths=("assets/orca.png", "assets/orca-glow.png"),
                 frame_ms=140):
        super().__init__()

        # Load frames (fallback draws a colored rect so class still works)
        self.frames = []
        for p in frame_paths:
            try:
                img = pygame.image.load(p).convert_alpha()
            except Exception as e:
                print(f"[NPC] Could not load '{p}': {e}")
                img = pygame.Surface((96, 64), pygame.SRCALPHA)
                img.fill((200, 40, 40, 255))
                pygame.draw.rect(img, (255, 255, 255, 255), (12, 22, 72, 20))
            self.frames.append(img)

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

        # Animation timing
        self.frame_ms = max(60, int(frame_ms))
        self._next_tick = pygame.time.get_ticks() + self.frame_ms

        # Movement/animation control
        self.speed = 4
        self._moving_this_frame = False  # set by move(), read by update()

    def update(self):
        """Advance animation only if move() was called this frame."""
        if not self._moving_this_frame:
            # Idle: hold on the first frame
            if self.frame_index != 0:
                self.frame_index = 0
                self.image = self.frames[self.frame_index]
            return

        now = pygame.time.get_ticks()
        if now >= self._next_tick:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self._next_tick = now + self.frame_ms

        # Reset for next tick; must move again to keep animating
        self._moving_this_frame = False

    def move(self, dx: int, dy: int, bounds: pygame.Rect | None = None):
        """Move sprite by dx, dy; clamp to bounds if provided. Triggers animation."""
        if dx or dy:
            self._moving_this_frame = True
            self.rect.move_ip(dx, dy)
            if bounds is not None:
                self.rect.clamp_ip(bounds)
