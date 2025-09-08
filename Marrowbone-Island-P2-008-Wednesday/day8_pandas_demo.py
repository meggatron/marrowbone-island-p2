import pandas as pd

# Load the CSV
df = pd.read_csv("npc_traits.csv")

# Show the full table
print("NPCs in the game:\n")
print(df)
#print(df[df["location"] == "Tide Pools"])
#loc = input("Enter a location to search: ")
#print(df[df["location"].str.lower() == loc.lower()])