# game/sprite_sasquatch.py
# a simple animated NPC sprite for Sasquatch with two frames (idle/bolts)
# NEW: auto-fit-to-height + animate-on-move (holds idle frame when still)

import pygame

class Sasquatch(pygame.sprite.Sprite):
    """
    Loads sasquatch1.png (idle) and sasquatch2.png (bolts).
    - target_height: scales both frames to this pixel height (keeps aspect).
    - If target_height is None, uses 'scale' multiplier instead.
    - Animation flips ONLY when the sprite actually moved since last update,
      which mimics “animate-when-walking” behavior.
    """
    def __init__(
        self,
        x: int,
        y: int,
        frame_ms: int = 180,
        scale: float = 0.75,         # used only if target_height is None
        target_height: int | None = None,  # NEW: fit-to-window helper
    ):
        super().__init__()
        self.frames = []

        # load both frames with alpha
        raw_frames = []
        for p in ("assets/sasquatch1.png", "assets/sasquatch2.png"):
            try:
                raw_frames.append(pygame.image.load(p).convert_alpha())
            except Exception:
                # fallback rectangle so class still works if asset missing
                img = pygame.Surface((220, 320), pygame.SRCALPHA)
                img.fill((150, 90, 40, 255))
                raw_frames.append(img)

        # scale: prefer target_height if provided; else apply scale multiplier
        def scale_img(img):
            if target_height is not None:
                h = target_height
                w = int(img.get_width() * (h / img.get_height()))
                return pygame.transform.smoothscale(img, (w, h))
            if scale != 1.0:
                w, h = img.get_width(), img.get_height()
                return pygame.transform.smoothscale(img, (int(w * scale), int(h * scale)))
            return img

        self.frames = [scale_img(img) for img in raw_frames]

        # timing + pose
        self.frame_ms = frame_ms
        self.frame_i = 0
        self.image = self.frames[self.frame_i]
        self.rect = self.image.get_rect(center=(x, y))

        # NEW: movement-aware animation
        self._accum = 0
        self._last_pos = self.rect.topleft  # detect motion between frames

    def update(self, dt_ms: int = 0):
        """
        Only animate when position changed since last update.
        dt_ms should come from clock.get_time() (locations pass this already).
        """
        moved = (self.rect.topleft != self._last_pos)
        self._last_pos = self.rect.topleft

        if not moved:
            # hold on idle frame when still
            if self.frame_i != 0:
                self.frame_i = 0
                self.image = self.frames[self.frame_i]
            return

        # moving → run the simple two-frame flip
        self._accum += dt_ms or self.frame_ms
        if self._accum >= self.frame_ms:
            self._accum = 0
            self.frame_i = (self.frame_i + 1) % len(self.frames)
            self.image = self.frames[self.frame_i]
