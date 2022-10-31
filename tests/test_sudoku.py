import unittest

from main.GameBoard import GameBoard, IllegalMoveError
from main.Sudoku import Sudoku, Guess
from main.BoardFactory import BoardFactory, Difficulty


class StubbedBoardFactory(BoardFactory):

    def generate_board(self, difficulty: Difficulty) -> GameBoard:
        return GameBoard([[0, 6, 1, 8, 4, 2, 7, 5, 3],
                          [8, 5, 7, 9, 6, 3, 2, 4, 1],
                          [2, 4, 3, 1, 5, 7, 9, 6, 8],
                          [1, 9, 6, 2, 8, 4, 3, 7, 5],
                          [7, 8, 5, 3, 9, 6, 1, 2, 4],
                          [3, 2, 4, 7, 1, 5, 8, 9, 6],
                          [6, 1, 9, 4, 2, 8, 5, 3, 7],
                          [5, 7, 8, 6, 3, 9, 4, 0, 2],
                          [4, 3, 2, 5, 7, 1, 6, 8, 9]],
                         {(0, 0, 9), (7, 7, 1)})


class SudokuTest(unittest.TestCase):
    s: Sudoku = None

    def setUp(self) -> None:
        self.s = Sudoku(StubbedBoardFactory())
        self.s.start_new_game(Difficulty.OFF)

    def test_can_create_new_game(self):
        game: Sudoku = Sudoku(StubbedBoardFactory())
        self.assertFalse(game.game_started())

        game.start_new_game(Difficulty.OFF)
        self.assertTrue(self.s.game_started())
        self.assertFalse(self.s.game_over())

    def test_wrong_number_guess_returns_false(self):
        self.assertFalse(self.s.guess_number(Guess(2, 2, 9)))

    def test_correct_number_guess_returns_true(self):
        self.assertTrue(self.s.guess_number(Guess(0, 0, 9)))

    def test_three_wrong_guesses_ends_game(self):
        self.s.guess_number(Guess(2, 2, 9))
        self.assertFalse(self.s.game_over())

        self.s.guess_number(Guess(2, 2, 9))
        self.assertFalse(self.s.game_over())

        self.s.guess_number(Guess(2, 2, 9))
        self.assertTrue(self.s.game_over())

    def test_move_outside_game_board_causes_error(self):
        with self.assertRaises(IllegalMoveError):
            self.s.guess_number(Guess(-1, -1, 9))

        with self.assertRaises(IllegalMoveError):
            self.s.guess_number(Guess(10, 10, 9))

    def test_user_board_can_be_returned(self):
        board: list[list[int]] = self.s.get_user_board()
        self.assertEqual(9, len(board))
        self.assertEqual(9, len(board[0]))
        self.assertEqual(int, type(board[0][0]))

    def test_user_board_contains_0_for_empty_space(self):
        board: list[list[int]] = self.s.get_user_board()
        row_nums = set([])
        for row in range(len(board)):
            for col in range(len(board[0])):
                row_nums.add(board[row][col])

        self.assertTrue(0 in row_nums)

    def test_can_win_game(self):
        self.s.guess_number(Guess(0, 0, 9))
        self.s.guess_number(Guess(7, 7, 1))
        self.assertTrue(self.s.is_winner())
        self.assertTrue(self.s.game_over())

    def test_after_a_win_game_game_isnt_started(self):
        self.s.guess_number(Guess(0, 0, 9))
        self.s.guess_number(Guess(7, 7, 1))
        self.assertTrue(self.s.is_winner())
        self.assertFalse(self.s.game_started())

    def test_can_print_board(self):
        board: str = """\
=======================================
|   | 6 | 1 || 8 | 4 | 2 || 7 | 5 | 3 |
| 8 | 5 | 7 || 9 | 6 | 3 || 2 | 4 | 1 |
| 2 | 4 | 3 || 1 | 5 | 7 || 9 | 6 | 8 |
============||===========||============
| 1 | 9 | 6 || 2 | 8 | 4 || 3 | 7 | 5 |
| 7 | 8 | 5 || 3 | 9 | 6 || 1 | 2 | 4 |
| 3 | 2 | 4 || 7 | 1 | 5 || 8 | 9 | 6 |
============||===========||============
| 6 | 1 | 9 || 4 | 2 | 8 || 5 | 3 | 7 |
| 5 | 7 | 8 || 6 | 3 | 9 || 4 |   | 2 |
| 4 | 3 | 2 || 5 | 7 | 1 || 6 | 8 | 9 |
=======================================
"""
        self.assertEqual(board, str(self.s))

