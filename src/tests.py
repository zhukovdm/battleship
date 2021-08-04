import unittest

from grid import Grid

# python -m unittest tests

class GridTest(unittest.TestCase):
    
    def test_grid_rows(self):
        g = Grid()
        self.assertEqual(g.rows, 10)

    def test_within_bounds_true(self):
        g = Grid()
        self.assertEqual(g.within_bounds(1, 1), True)

    def test_within_bounds_false(self):
        g = Grid()
        self.assertEqual(g.within_bounds(-1, -1), False)

    def test_get_view_unknown_cell(self):
        g = Grid()
        v = g.get_view(1, 1)
        self.assertEqual(v, Grid.unknown_cell)

class PlayerTest(unittest.TestCase):

    def test_init(self):
        self.assertEqual(True, True)

    

class GameTest(unittest.TestCase):

    def test_init(self):
        self.assertEqual(True, True)

    

if __name__ == "__main__":
    unittest.main()
