import unittest 
import os 
import sys
from context import src 
from src import tile 

class testTile(unittest.TestCase):

    def test_behavior(self):
        tile1 = tile.Tile() 

        tile1.set_flag()
        self.assertTrue(tile1.flagged)
        self.assertEqual("!", tile1.to_s())

        tile1.set_flag()
        self.assertFalse(tile1.flagged)
        self.assertEqual("*", tile1.to_s())

        tile1.reveal()
        self.assertEqual("_", tile1.to_s())

        tile1.add_adj_bomb()
        self.assertEqual(1, tile1.adj_bombs)
        self.assertFalse(tile1.is_bomb())
        self.assertEqual("1", tile1.to_s())

        tile1.add_adj_bomb()
        self.assertEqual(2, tile1.adj_bombs)
        self.assertFalse(tile1.is_bomb()) 
        self.assertEqual("2", tile1.to_s())

        tile1.convert_to_bomb() 
        self.assertTrue(tile1.is_bomb())   
        self.assertEqual("B", tile1.to_s())

    def test_constructor(self):
        tile1 = tile.Tile()
        self.assertEqual(0, tile1.adj_bombs)
        self.assertFalse(tile1.revealed)
        self.assertEqual("*", tile1.to_s())
        self.assertFalse(tile1.flagged)

    def test_revealed(self):
        tile1 = tile.Tile()
        tile1.reveal()
        self.assertTrue(tile1.revealed)

if __name__ == '__main__':
    unittest.main()