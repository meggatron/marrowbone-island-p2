import pygame
import sys

class GuiHandler:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Return to Marrowbone")
        self.font = pygame.font.SysFont(None, 28)
        self.clock = pygame.time.Clock()

        self.input_text = ""
        self.display_lines = []

        self.input_rect = pygame.Rect(20, height - 50, width - 40, 30)
        self.output_rect = pygame.Rect(20, 20, width - 40, height - 90)

    def display(self, text):
        # split and store lines
        for line in text.strip().split("\n"):
            self.display_lines.append(line)
        if len(self.display_lines) > 20:
            self.display_lines = self.display_lines[-20:]  # keep last 20 lines
        self._render()

    def log_room(self, location):
        with open("log.txt", "a") as log:
            log.write(f"Entered {location}\n")

    def get_input(self, prompt):
        self.display(prompt)
        self.input_text = ""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        user_input = self.input_text.strip()
                        self.input_text = ""
                        self.display(f"> {user_input}")
                        return user_input
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode

            self._render()
            self.clock.tick(30)

    def _render(self):
        self.screen.fill((20, 30, 50))

        # wrap and flatten all lines for width
        wrapped_lines = []
        for line in self.display_lines:
            words = line.split()
            if not words:
                wrapped_lines.append("")
                continue

            current_line = words[0]
            for word in words[1:]:
                test_line = f"{current_line} {word}"
                if self.font.size(test_line)[0] <= self.output_rect.width - 20:
                    current_line = test_line
                else:
                    wrapped_lines.append(current_line)
                    current_line = word
            wrapped_lines.append(current_line)

        # calculate max number of lines that fit without overlapping input box
        line_height = 30
        available_height = self.input_rect.top - self.output_rect.top - 10
        max_lines = available_height // line_height

        # keep only last N lines
        visible_lines = wrapped_lines[-max_lines:]

        # draw output text
        y = self.output_rect.y + 5
        for line in visible_lines:
            txt = self.font.render(line, True, (255, 200, 200))
            self.screen.blit(txt, (self.output_rect.x + 10, y))
            y += line_height

        # draw input box
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        input_surface = self.font.render(self.input_text, True, (255, 255, 255))
        self.screen.blit(input_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        pygame.display.flip()
