# creature is the superclass, Shrimp is a subclass that inherits from it
class Creature:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} says something cryptic."


class Shrimp(Creature):
    def speak(self):
        return f"{self.name} says: 'I come from Bremerton.'"


class Duck:
    # not inheriting from Creature, here for duck typing
    def speak(self):
        return "Quack."


def make_it_talk(animal):
    # works as long as 'animal' has a .speak() method
    print(animal.speak())


# Duck typing in action
make_it_talk(Shrimp("Giant Shrimp"))  # I come from Bremerton.
make_it_talk(Duck())                  # Quack.
