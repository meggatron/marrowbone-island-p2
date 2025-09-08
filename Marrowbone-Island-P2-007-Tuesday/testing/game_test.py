import unittest

 from game import Game   # <-- later we’ll import the real Game class here

# A tiny placeholder Game class, comment out when you use import above
# You can replace this with your own class later.

class Game:
    def __init__(self):
        # Start the game at the "dock"
        self.current_location = "dock"


class TestGame(unittest.TestCase):
    # Each method beginning with "test_" is one unit test
    def test_change_location(self):
        # Create a new game object
        game = Game()

        # Change its location
        game.current_location = "forest"

        # Check that the location actually changed
        # If not, this test will FAIL with AssertionError
        self.assertEqual(game.current_location, "cave")


# This runs the test when we run the file directly
if __name__ == "__main__":
    unittest.main()
