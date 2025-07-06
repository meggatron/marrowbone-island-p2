from game import locations, player

def intro():
    player.player_name = input("What is your name, adventurer? ")
    print(f"Welcome, {player.player_name}! Your adventure begins now.")

def main():
    intro()
    current_location = "dock"

    while True:
        location_func = locations.locations[current_location]
        result = location_func()  # call the location function

        if result == "end":
            break  # stop the game loop if the game ended

        print("\nPossible locations to go:")
        for loc in locations.locations:
            if loc != "end":
                print(f" - {loc.replace('_', ' ').title()}")

        next_location = input("Where do you want to go next? ").lower().replace(" ", "_")

        if next_location in locations.locations and next_location != "end":
            current_location = next_location
        else:
            print("Invalid location. Try again.")

        print(f"\nCurrent Inventory: {', '.join(player.inventory) if player.inventory else 'None'}")
        print(f"NPCs Met: {', '.join(player.npcs) if player.npcs else 'None'}")
        print(f"Gifts: {', '.join(player.gifts) if player.gifts else 'None'}\n")

    print("Thanks for playing!")

if __name__ == "__main__":
    main()
