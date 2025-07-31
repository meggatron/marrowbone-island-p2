class Creature:
    def __init__(self, name, location, gift):
        self.name = name
        self.location = location
        self.gift = gift

    def speak(self):
        return f"You meet {self.name} at the {self.location}."

    def give_gift(self):
        return f"{self.name} gives you the power of {self.gift}."
