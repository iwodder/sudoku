import unittest

from main.BoardFactory import GameBoard


class GameBoardTest(unittest.TestCase):

    def test_create_board(self):
        board: GameBoard = GameBoard([[0]], {(0, 0, 1)})
        board.guess(0, 0, 1)
        self.assertTrue(board.is_solved())

    def test_boards_equal_based_on_grid(self):
        board: GameBoard = GameBoard([[0]], {(0, 0, 1)})
        board1: GameBoard = GameBoard([[0]], {(0, 0, 1)})
        self.assertEqual(board, board1)

    def test_boards_not_equal_based_on_grid(self):
        board: GameBoard = GameBoard([[0]], {(0, 0, 1)})
        board1: GameBoard = GameBoard([[1]], {(0, 0, 1)})
        self.assertNotEqual(board, board1)

    def test_real_board(self):
        grid = [[0, 6, 1, 8, 4, 2, 7, 5, 3],
                [8, 5, 7, 9, 6, 3, 2, 4, 1],
                [2, 4, 3, 1, 5, 7, 9, 6, 8],
                [0, 9, 6, 2, 8, 4, 3, 7, 5],
                [7, 8, 5, 3, 9, 6, 1, 2, 4],
                [3, 2, 4, 7, 1, 5, 8, 9, 6],
                [6, 1, 9, 4, 2, 8, 5, 3, 7],
                [5, 7, 8, 6, 3, 9, 4, 1, 2],
                [4, 3, 2, 5, 7, 1, 6, 8, 0]]
        moves = {(0, 0, 9), (3, 0, 1), (8, 8, 9)}
        board: GameBoard = GameBoard(grid, moves)

        board.guess(0, 0, 9)
        board.guess(3, 0, 1)
        board.guess(8, 8, 9)

        self.assertTrue(board.is_solved())
