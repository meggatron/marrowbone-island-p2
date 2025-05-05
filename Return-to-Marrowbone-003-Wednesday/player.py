def intro(gui):
    with open("intro.txt", "r") as f:
        for line in f:
            gui.display(line.strip())

    name = gui.get_input("what is your name, adventurer? > ")
    gui.display(f"welcome, {name}. your quest begins now...\n")
    return name
