from collections import deque
import time

npc_queue = deque()
undo_stack = []

npc_queue.append({"npc": "Shrimp", "action": "speak", "message": "Hey there, traveler!"})
npc_queue.append({"npc": "Sasquatch", "action": "give_item", "item": "Magnetic Boots"})
npc_queue.append({"npc": "Orca", "action": "speak", "message": "The tide is turning..."})

def process_event(event):
    if event["action"] == "speak":
        print(f'{event["npc"]} says: {event["message"]}')
    elif event["action"] == "give_item":
        print(f'{event["npc"]} gives you: {event["item"]}')

def undo():
    if undo_stack:
        last_event = undo_stack.pop()
        print(f'Undoing event: {last_event}')
    else:
        print("Nothing to undo.")

while npc_queue:
    event = npc_queue.popleft()
    process_event(event)
    undo_stack.append(event)
    time.sleep(1)

# Example undo call
undo()
undo()
undo()
undo()