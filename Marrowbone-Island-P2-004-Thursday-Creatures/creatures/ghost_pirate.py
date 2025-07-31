from .base import Creature

class GhostPirate(Creature):
    def __init__(self):
        super().__init__("Ghost Pirate", "Shipwreck", "lantern")

    def speak(self):
        return "'Yarrrr!' the Ghost Pirate bellows. 'I left this in me other pants!'"
