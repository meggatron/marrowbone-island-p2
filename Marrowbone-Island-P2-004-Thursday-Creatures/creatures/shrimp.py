from .base import Creature

class Shrimp(Creature):
    def __init__(self):
        super().__init__("Giant Shrimp", "Boat House", "sling shot")

    def speak(self):
        return "The Giant Shrimp snaps its claws. 'Take this, you’ll need it.'"
