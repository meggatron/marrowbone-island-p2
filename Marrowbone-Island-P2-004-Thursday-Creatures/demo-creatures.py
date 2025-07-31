from creatures.shrimp import Shrimp
from creatures.sasquatch import Sasquatch
from creatures.loowit import Loowit
from creatures.ghost_pirate import GhostPirate


if __name__ == "__main__":
    creatures = [Shrimp(), Sasquatch(), Loowit(), GhostPirate()]
    for c in creatures:
        print(c.speak())
        print(c.give_gift())
        print("---")
