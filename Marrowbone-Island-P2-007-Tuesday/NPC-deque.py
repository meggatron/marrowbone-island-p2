from collections import deque
import time

# Define a queue of future NPC events
npc_queue = deque()

# Add events (could be more complex in your actual game)
npc_queue.append({"npc": "Shrimp", "action": "speak", "message": "Hey there, traveler!"})
npc_queue.append({"npc": "Sasquatch", "action": "give_item", "item": "Magnetic Boots"})
npc_queue.append({"npc": "Orca", "action": "speak", "message": "The tide is turning..."})

# Simulate processing events over time
while npc_queue:
    event = npc_queue.popleft()

    if event["action"] == "speak":
        print(f'{event["npc"]} says: {event["message"]}')
    elif event["action"] == "give_item":
        print(f'{event["npc"]} gives you: {event["item"]}')

    time.sleep(1)  # Simulate delay between events
