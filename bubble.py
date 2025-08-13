backpack = ["map", "string", "lantern", "magnet"]

for i in range(len(backpack)):
    for j in range(0, len(backpack)-i-1):
        if backpack[j] > backpack[j+1]:
            backpack[j], backpack[j+1] = backpack[j+1], backpack[j]

print("Sorted: ", backpack)

