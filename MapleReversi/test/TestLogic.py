import unittest
import numpy as np
import sys

sys.path.append('..')
from OthelloLogic import Board

class InitTest(unittest.TestCase):
    
    def test_four_board(self):
        four_board = Board(4)
        ans = np.array([
            [0,  0,  0, 0],
            [0, -1,  1, 0],
            [0,  1, -1, 0],
            [0,  0,  0, 0]
        ])
        self.assertTrue(np.array_equal(four_board.pieces, ans))
    
    def test_eight_board(self):
        eight_board = Board(8)
        ans = np.array([
            [0, 0, 0,  0,  0, 0, 0, 0],
            [0, 0, 0,  0,  0, 0, 0, 0],
            [0, 0, 0,  0,  0, 0, 0, 0],
            [0, 0, 0, -1,  1, 0, 0, 0],
            [0, 0, 0,  1, -1, 0, 0, 0],
            [0, 0, 0,  0,  0, 0, 0, 0],
            [0, 0, 0,  0,  0, 0, 0, 0],
            [0, 0, 0,  0,  0, 0, 0, 0]
        ])
        self.assertTrue(np.array_equal(eight_board.pieces, ans))
    
    def test_seven_board(self):
        with self.assertRaises(ValueError):
            Board(7)
    
    def test_obstacles_error(self):
        with self.assertRaises(ValueError):
            Board(6, [(1, 1), (1, 1)])
        
        with self.assertRaises(ValueError):
            Board(6, [(2, 2)])
        
        with self.assertRaises(ValueError):
            Board(6, [(2, 3)])
    
    def test_obstacles(self):
        board = Board(6, [(1, 1), (0, 0), (4, 5)])
        ans = np.array([
            [2, 0,  0,  0, 0, 0],
            [0, 2,  0,  0, 0, 0],
            [0, 0, -1,  1, 0, 0],
            [0, 0,  1, -1, 0, 0],
            [0, 0,  0,  0, 0, 2],
            [0, 0,  0,  0, 0, 0],
        ])
        self.assertTrue(np.array_equal(board.pieces, ans))


if __name__ == '__main__':
    unittest.main()