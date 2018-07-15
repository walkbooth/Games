import unittest 
import os 
import sys
from src import grid
import random 
from random import Random 
from mock import patch 
class testTile(unittest.TestCase):

    def setUp(self):
        self.random = Random(916)

    def test_constructor(self):
        grid1AllBomb = grid.Grid(1, 1, 1)
        self.assertEqual("* \n", grid1AllBomb.to_s())
        self.assertEqual(1, grid1AllBomb.game_state())
        self.assertTrue(grid1AllBomb.reveal_tile(0, 0))
        self.assertEqual("B \n", grid1AllBomb.to_s())
        self.assertEqual(-1, grid1AllBomb.game_state())

        grid4AllBomb = grid.Grid(2, 2, 4)
        self.assertEqual("* * \n* * \n", grid4AllBomb.to_s())
        self.assertEqual(1, grid4AllBomb.game_state())
        self.assertTrue(grid4AllBomb.reveal_tile(1, 1))
        self.assertEqual("* * \n* B \n", grid4AllBomb.to_s())
        self.assertEqual(-1, grid4AllBomb.game_state())


        grid1NoBomb = grid.Grid(1, 1, 0)
        self.assertEqual("* \n", grid1NoBomb.to_s())
        self.assertFalse(grid1NoBomb.reveal_tile(0, 0))
        self.assertEqual("_ \n", grid1NoBomb.to_s())
        self.assertEqual(1, grid1NoBomb.game_state())
        
        grid4NoBomb = grid.Grid(2, 2, 0)
        self.assertEqual("* * \n* * \n", grid4NoBomb.to_s())
        self.assertFalse(grid4NoBomb.reveal_tile(0, 0))
        self.assertEqual("_ _ \n_ _ \n", grid4NoBomb.to_s())
        self.assertEqual(1, grid4NoBomb.game_state())        

        # Testing with bad parameters
        with self.assertRaises(ValueError):
            grid.Grid(0, 1, 1)
        with self.assertRaises(ValueError):
            grid.Grid(1, 0, 1)
        with self.assertRaises(ValueError):
            grid.Grid(1, 1, 2)
        with self.assertRaises(ValueError):
            grid.Grid("adsf", "sda", 1)

    @patch('src.grid.random')
    def test_sample_game(self, random):
        random.sample._mock_side_effect = self.random.sample
        gridCustom1 = grid.Grid(3, 3, 3)
        self.assertEqual("* * * \n* * * \n* * * \n", gridCustom1.to_s())
        self.assertEqual(0, gridCustom1.game_state())
        self.assertFalse(gridCustom1.reveal_tile(0, 0))
        self.assertEqual("_ _ _ \n2 3 2 \n* * * \n", gridCustom1.to_s())
        self.assertEqual(1, gridCustom1.game_state())
        self.assertTrue(gridCustom1.reveal_tile(2, 2))
        self.assertEqual("_ _ _ \n2 3 2 \n* * B \n", gridCustom1.to_s())
        self.assertEqual(-1, gridCustom1.game_state())
        self.assertTrue(gridCustom1.reveal_tile(1, 2))
        self.assertEqual("_ _ _ \n2 3 2 \n* B B \n", gridCustom1.to_s())
        self.assertEqual(-1, gridCustom1.game_state())
        self.assertTrue(gridCustom1.reveal_tile(0, 2))
        self.assertEqual("_ _ _ \n2 3 2 \nB B B \n", gridCustom1.to_s())
        self.assertEqual(-1, gridCustom1.game_state())

        gridCustom2 = grid.Grid(3, 3, 3)
        self.assertEqual("* * * \n* * * \n* * * \n", gridCustom2.to_s())
        self.assertFalse(gridCustom2.reveal_tile(1, 0))
        self.assertEqual("* 1 * \n* * * \n* * * \n", gridCustom2.to_s())
        self.assertFalse(gridCustom2.reveal_tile(0, 0))
        self.assertEqual("1 1 * \n* * * \n* * * \n", gridCustom2.to_s())
        self.assertFalse(gridCustom2.reveal_tile(2, 0))
        self.assertEqual("1 1 _ \n* 3 2 \n* * * \n", gridCustom2.to_s())
        gridCustom2.flag_tile(0, 1)
        self.assertEqual("1 1 _ \n! 3 2 \n* * * \n", gridCustom2.to_s())
        self.assertFalse(gridCustom2.reveal_tile(0, 2))
        self.assertEqual("1 1 _ \n! 3 2 \n2 * * \n", gridCustom2.to_s())
        self.assertEqual(1, gridCustom2.game_state())


        gridCustom3 = grid.Grid(3, 3, 3)
        self.assertTrue(gridCustom3.reveal_tile(1, 1))
        self.assertEqual("* * * \n* B * \n* * * \n", gridCustom3.to_s())

        gridCustom4 = grid.Grid(3, 3, 3)
        self.assertEqual("* * * \n* * * \n* * * \n", gridCustom4.to_s())
        self.assertFalse(gridCustom4.reveal_tile(1, 0))
        self.assertEqual("* 2 * \n* * * \n* * * \n", gridCustom4.to_s())
        self.assertFalse(gridCustom4.reveal_tile(2, 0))
        self.assertEqual("* 2 1 \n* * * \n* * * \n", gridCustom4.to_s())
        self.assertFalse(gridCustom4.reveal_tile(0, 1))
        self.assertEqual("* 2 1 \n3 * * \n* * * \n", gridCustom4.to_s())
        self.assertFalse(gridCustom4.reveal_tile(2, 1))
        self.assertEqual("* 2 1 \n3 * 2 \n* * * \n", gridCustom4.to_s())
        self.assertFalse(gridCustom4.reveal_tile(0, 2))
        self.assertEqual("* 2 1 \n3 * 2 \n2 * * \n", gridCustom4.to_s())
        self.assertFalse(gridCustom4.reveal_tile(2, 2))
        self.assertEqual("* 2 1 \n3 * 2 \n2 * 2 \n", gridCustom4.to_s())

        gridCustom5 = grid.Grid(4, 4, 4, 0, 0)
        self.assertEqual("* * * * \n* * * * \n* * * * \n* * * * \n", gridCustom5.to_s())
        self.assertFalse(gridCustom5.reveal_tile(0, 0))
        self.assertEqual("_ _ 1 * \n_ _ 2 * \n1 1 4 * \n* * * * \n", gridCustom5.to_s())
        self.assertEqual(0, gridCustom5.game_state())
        self.assertFalse(gridCustom5.reveal_tile(3, 0))
        self.assertEqual(0, gridCustom5.game_state())
        self.assertFalse(gridCustom5.reveal_tile(2, 3))
        self.assertEqual(0, gridCustom5.game_state())
        self.assertFalse(gridCustom5.reveal_tile(0, 3))
        self.assertEqual(1, gridCustom5.game_state())        
        self.assertEqual("_ _ 1 1 \n_ _ 2 * \n1 1 4 * \n1 * 3 * \n", gridCustom5.to_s())

if __name__ == '__main__':
    unittest.main()