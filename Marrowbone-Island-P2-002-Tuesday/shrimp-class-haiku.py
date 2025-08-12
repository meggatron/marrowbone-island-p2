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
            "Here is your haiku, friend."
        ]

    def recite_poem(self, noun, verb, adjective):
        return [
            f"   {noun} in moonlight",
            f"   {verb} through the tidepool",
            f"   the sea is {adjective}"
        ]

# get info from the player
shrimp_name = input("give the shrimp a name > ") or "Sebastian"
shrimp_mood = input("how does the shrimp feel today? > ") or "reflective"
poem_noun = input("give the shrimp a noun > ") or "kelp"
poem_verb = input("give the shrimp a verb ending in -ing > ") or "drifting"
poem_adj = input("describe the sea in one word > ") or "endless"

# create the shrimp
shrimp = Shrimp(shrimp_name, shrimp_mood)

# combine the lines
lines = shrimp.intro_line() + shrimp.recite_poem(poem_noun, poem_verb, poem_adj)

# print them
print("\n--- the shrimp speaks ---\n")
for line in lines:
    print(line)
