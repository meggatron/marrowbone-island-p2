import pygame, sys, math

pygame.init()
W, H = 960, 540
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
pygame.display.set_caption("Basic Animations")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (255,   0,   0),  # red
    (0,   255,   0),  # green
    (0,     0, 255),  # blue
    (255, 255,   0)   # yellow
]

font = pygame.font.SysFont(None, 32)
font_small = pygame.font.SysFont(None, 28)

class RectSprite:
    def __init__(self, color, size, center, label, mode):
        self.base_image = pygame.Surface(size, pygame.SRCALPHA)
        self.base_image.fill(color)
        self.size = size
        self.base_center = pygame.Vector2(center)
        self.center = pygame.Vector2(center)
        self.angle = 0.0
        self.scale = 1.0
        self.active = False
        self.label = label
        self.mode = mode

        # --- Mode 1: jump up/down ---
        self.jump_height = 60
        self.jump_period = 0.6   # seconds for full up/down
        self.jump_timer = 0.0
        self.jump_up = False

        # --- Mode 2: zoom pulse ---
        self.zoom_lo, self.zoom_hi = 0.7, 2.0
        self.zoom_period = 1.0
        self.zoom_timer = 0.0

        # --- Mode 3: rotate back & forth ---
        self.rot_max = 25        # degrees
        self.rot_half_period = 0.5
        self.rot_timer = 0.0
        self.rot_side = 1        # +1 / -1

        # --- Mode 4: full spin + arc (up → slight right at top → down) ---
        self.spin_dps = 360      # degrees per second
        self.arc_height = 100
        self.arc_right = 40
        self.arc_period = 2.0
        self.arc_timer = 0.0

    def toggle(self):
        self.active = not self.active
        if not self.active:
            # reset to base when turning off
            self.center = self.base_center.copy()
            self.angle = 0.0
            self.scale = 1.0
            self.jump_timer = 0.0
            self.jump_up = False
            self.zoom_timer = 0.0
            self.rot_timer = 0.0
            self.rot_side = 1
            self.arc_timer = 0.0

    def update(self, dt):
        if not self.active:
            return

        if self.mode == 1:
            # Jump up/down: alternate between base y and base y - jump_height
            self.jump_timer += dt
            half = self.jump_period * 0.5
            if self.jump_timer >= half:
                self.jump_timer -= half
                self.jump_up = not self.jump_up
            self.center.x = self.base_center.x
            self.center.y = self.base_center.y - (self.jump_height if self.jump_up else 0)

        elif self.mode == 2:
            # Zoom pulse between zoom_lo and zoom_hi (triangle wave)
            self.zoom_timer = (self.zoom_timer + dt) % self.zoom_period
            phase = self.zoom_timer / self.zoom_period  # 0..1
            s = phase*2 if phase < 0.5 else (1 - phase)*2  # 0->1->0
            self.scale = self.zoom_lo + (self.zoom_hi - self.zoom_lo) * s

        elif self.mode == 3:
            # Rotate back & forth: hold +max, then -max
            self.rot_timer += dt
            if self.rot_timer >= self.rot_half_period:
                self.rot_timer -= self.rot_half_period
                self.rot_side *= -1
            self.angle = self.rot_max * self.rot_side

        elif self.mode == 4:
            # Full rotation around center + arc path
            self.angle = (self.angle + self.spin_dps * dt) % 360
            self.arc_timer = (self.arc_timer + dt) % self.arc_period
            phase = self.arc_timer / self.arc_period               # 0..1
            y_off = -self.arc_height * math.sin(math.pi * phase)   # up then down
            x_off =  self.arc_right  * math.sin(math.pi * phase)   # little right at top
            self.center.x = self.base_center.x + x_off
            self.center.y = self.base_center.y + y_off

    def draw(self, surf):
        img = self.base_image
        # Apply scale then rotation around center
        if self.scale != 1.0:
            w, h = img.get_size()
            img = pygame.transform.smoothscale(img, (int(w*self.scale), int(h*self.scale)))
        if self.angle != 0.0:
            img = pygame.transform.rotate(img, self.angle)

        rect = img.get_rect(center=(int(self.center.x), int(self.center.y)))
        surf.blit(img, rect)

        # number label under original base position
        label_surf = font_small.render(str(self.label), True, WHITE)
        label_rect = label_surf.get_rect(center=(int(self.base_center.x),
                                                 int(self.base_center.y + self.size[1]//2 + 24)))
        surf.blit(label_surf, label_rect)


# Layout
spacing = W // 5
centers = [(spacing * 1, H*0.6),
           (spacing * 2, H*0.6),
           (spacing * 3, H*0.6),
           (spacing * 4, H*0.6)]
size = (80, 160)

# Build four with modes 1..4
rects = [
    RectSprite(COLORS[0], size, centers[0], 1, mode=1),  # jump up/down
    RectSprite(COLORS[1], size, centers[1], 2, mode=2),  # zoom
    RectSprite(COLORS[2], size, centers[2], 3, mode=3),  # rotate back/forth
    RectSprite(COLORS[3], size, centers[3], 4, mode=4),  # rotate + arc
]

instruction = font.render("Press 1–4 to start/stop animations", True, WHITE)

# Main loop
while True:
    dt = clock.tick(60) / 1000.0
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_1: rects[0].toggle()
            if e.key == pygame.K_2: rects[1].toggle()
            if e.key == pygame.K_3: rects[2].toggle()
            if e.key == pygame.K_4: rects[3].toggle()

    for r in rects:
        r.update(dt)

    screen.fill(BLACK)
    screen.blit(instruction, instruction.get_rect(center=(W//2, 24)))
    for r in rects:
        r.draw(screen)

    pygame.display.flip()
