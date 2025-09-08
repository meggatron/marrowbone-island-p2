import unittest   # bring in python's testing framework

# a tiny function we want to test
def add(a, b):
    return a + b

# a test class that inherits from unittest.testcase
class testmath(unittest.TestCase):
    # every method starting with "test_" will run as a unit test
    def test_add(self):
        # check that add(2, 3) returns 5
        # if it's not 5, the test will fail
        self.assertEqual(add(2, 3), 5)

# runs tests when this file is executed directly
if __name__ == "__main__":
    unittest.main()
