import pygame

# define the shrimp class
class Shrimp:
    def __init__(self, name="Sebastian", mood="reflective"):
        self.name = name
        self.mood = mood
        self.job = "giant shrimp living in a laundry room in Bremerton"

    def intro_line(self):
        return [
            f"Hi, my name is {self.name}.",
            f"I am a {self.job}.",
            f"Today I feel {self.mood}.",
            f"Here is your haiku, friend."
        ]

    def recite_poem(self, noun, verb, adjective):
        return [
            f"   {noun} in moonlight",
            f"   {verb} through the tidepool",
            f"   the sea is {adjective}"
        ]

# get info from the player
name = input("give the shrimp a name > ")
mood = input("how does the shrimp feel today? > ")
noun = input("give the shrimp a noun > ")
verb = input("give the shrimp a verb ending in -ing > ")
adjective = input("describe the sea in one word > ")

# create the shrimp
shrimp = Shrimp(name, mood)

# combine the lines
lines = shrimp.intro_line() + shrimp.recite_poem(noun, verb, adjective)

# set up pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("the shrimp speaks")

font = pygame.font.SysFont(None, 36)
bg_color = (20, 30, 50)
text_color = (255, 200, 200)
rendered = [font.render(line, True, text_color) for line in lines]

# game loop
running = True
while running:
    screen.fill(bg_color)
    for i, line in enumerate(rendered):
        screen.blit(line, (50, 100 + i * 50))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()