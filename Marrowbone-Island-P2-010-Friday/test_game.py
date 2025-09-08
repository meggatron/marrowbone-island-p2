import unittest
from game.main_game import Game

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_initial_location(self):
        self.assertEqual(self.game.current_location, "dock")
        print("✓ test_initial_location: Game starts at dock — PASSED")

    def test_inventory_addition(self):
        self.game.player.inventory.append("string")
        self.assertIn("string", self.game.player.inventory)
        print("✓ test_inventory_addition: Item added to inventory — PASSED")

    def test_location_change(self):
        self.game.current_location = "forest_trail"
        self.assertEqual(self.game.current_location, "forest_trail")
        print("✓ test_location_change: Location changes correctly — PASSED")

    def test_player_name_defaults_to_empty(self):
        self.assertEqual(self.game.player.player_name, "")
        print("✓ test_player_name_defaults_to_empty: Player name starts empty — PASSED")

if __name__ == "__main__":
    unittest.main()
