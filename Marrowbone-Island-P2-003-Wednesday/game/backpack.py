# game/backpack.py

class Backpack:
    def __init__(self): self.items = []

    def add_item(self, item):
        if item not in self.items: self.items.append(item)

    def view_sorted(self):
        if not self.items: print("Your backpack is empty.")
        else:
            print("Your inventory:")
            for it in sorted(self.items): print(f" - {it}")

    def search_item(self, name):
        for it in self.items:
            if it.lower() == name.lower():
                print(f"You have the {name}."); return True
        print(f"The {name} isn’t here."); return False

    def menu(self):
        while True:
            print("\n1. View sorted inventory\n2. Search for an item\n3. Close backpack")
            choice = input("> ").strip().lower()
            if choice == "1": self.view_sorted()
            elif choice == "2":
                item = input("What item are you looking for? ").strip()
                if item: self.search_item(item)
            elif choice == "3":
                print("You close your backpack."); return
            else: print("The backpack rustles... but offers no answer.")
