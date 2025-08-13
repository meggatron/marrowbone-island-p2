class Shrimp:
    def __init__(self, name, mood):
        self.name = name
        self.mood = mood
    #def speak(self):
       # return f"{self.name} speaks in a  {self.mood} tone."
    def intro_line(self):
        return [
            f"Hi, my name is {self.name}!",
            f"Today I feel {self.mood}!",
            f"Here is your haiku, Friend."
        ]

    def recite_poem(self, noun, verb, adjective):
        return  [
            f" {noun} in moonlight"
            f" {verb} through the tidepool"
            f" the sea is {adjective}"
        ]

shrimp_name = input("give the shrimp a name >") or "Sebastian"
shrimp_mood = input("how does the shrimp feel today? >") or "reflective"
poem_noun = input("give the shrimp a noun >") or "kelp"
poem_verb = input("give the shrimp a verb ending in -ing >") or "drifting"
poem_adj = input("describe the sea in one word >") or "endless"

shrimp = Shrimp(shrimp_name, shrimp_mood)

lines = shrimp.intro_line() + shrimp.recite_poem(poem_noun, poem_verb, poem_adj)

print("\n--- the Shrimp speaks  --\n")
for line in lines:
    print(line)