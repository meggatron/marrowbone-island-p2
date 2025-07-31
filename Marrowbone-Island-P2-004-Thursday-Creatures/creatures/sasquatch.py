from .base import Creature

class Sasquatch(Creature):
    def __init__(self):
        super().__init__("Sasquatch", "Cave", "magnetism")

    def give_gift(self):
        return "Sasquatch waves a hand. You feel a strange pull toward metal."
