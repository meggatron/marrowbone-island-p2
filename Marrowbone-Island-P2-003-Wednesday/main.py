#Lists, Searching & Sorting


from game import locations, player

def intro():
    with open("assets/intro.txt", "r") as f:
        for line in f:
            print(line.strip())
    player.player_name = input("What is your name, adventurer? > ")
    print(f"Welcome, {player.player_name}. Your quest begins now...")
    print("(Tip: type 'backpack' at any prompt to manage your items.)")

def main():
    intro()
    current_location = 'dock'

    while current_location != 'end':
        current_location = locations.locations[current_location](player.player_name)

if __name__ == "__main__":
    main()
