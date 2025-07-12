import random

def create_npc(creature_type):
    if creature_type == "shrimp":
        return {"type": "shrimp", "says": "The laundry is clean."}
    elif creature_type == "orca":
        return {"type": "orca", "says": "Bubble."}
    elif creature_type == "pirate":
        return {"type": "pirate", "says": "Aye."}
    else:
        return {"type": "unknown", "says": "..."}

# List of creature types
creatures = ["shrimp", "orca", "pirate"]

# Pick one at random
chosen = random.choice(creatures)

# Create and display the NPC
npc = create_npc(chosen)
print(f"You met a {npc['type']} who says: \"{npc['says']}\"")