from player import intro
from locations import locations

def main():
    player_name = intro()
    current_location = 'dock'

    while current_location != 'end':
        current_location = locations[current_location](player_name)

if __name__ == "__main__":
    main()
