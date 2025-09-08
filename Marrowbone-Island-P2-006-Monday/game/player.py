# game/player.py
# replaced player.py globals with a Player class (name, inventory, npcs, gifts)

# player has-a backpack (composition). keep "inventory" working via a property.
class Backpack:
    def __init__(self, items=None):
        self.items = list(items) if items is not None else []

# Player is a class → Game has-a Player (composition)
# avoids global state, lets us make fresh players, easier to test
class Player:
    def __init__(self, name: str = ""):
        self.name = name        # player identity

        # player has-a backpack (composition). We store items on the backpack,
        # but expose them via the inventory property for compatibility.
        self.backpack = Backpack()

        self.npcs = []          # characters met
        self.gifts = []         # powers/abilities gained

    @property
    def inventory(self):
        # compatibility: old code that uses player.inventory still works
        return self.backpack.items

    @inventory.setter
    def inventory(self, items):
        # allow assigning a whole list (e.g., during loads/tests)
        self.backpack.items = list(items)
