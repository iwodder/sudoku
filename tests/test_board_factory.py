import unittest
from main.BoardFactory import BoardFactory, BoardFactoryImpl, GameBoard, Difficulty


class BoardFactoryTest(unittest.TestCase):

    def setUp(self) -> None:
        self.bf: BoardFactory = BoardFactoryImpl()

    def test_two_boards_not_equal(self):
        board1: GameBoard = self.bf.generate_board(Difficulty.OFF)
        board2: GameBoard = self.bf.generate_board(Difficulty.OFF)
        self.assertNotEqual(board1, board2, "Boards shouldn't be equal")

    def test_generated_board_is_valid(self):
        board: list[list[int]] = self.bf.generate_board(Difficulty.OFF).get_board()
        self.assertTrue(self.is_valid(board), self.create_msg(board))

    def test_invalid_placement_outside_of_board(self):
        board: [[]] = list(list())
        self.assertFalse(self.bf.is_valid_place(board, 1, 1, 1))

    def test_valid_place(self):
        board: [[]] = list(list())
        self.assertFalse(self.bf.is_valid_place(board, 0, 0, 1))

    def test_invalid_place_in_row_already_filled(self):
        self.assertFalse(self.bf.is_valid_place([[1, 0, 0]], 0, 0, 1))
        self.assertFalse(self.bf.is_valid_place([[0, 1, 0]], 0, 1, 1))
        self.assertFalse(self.bf.is_valid_place([[0, 0, 1]], 0, 2, 1))

    def test_invalid_place_in_row_already_has_number(self):
        self.assertFalse(self.bf.is_valid_place([[1, 0, 0]], 0, 2, 1))

    def test_invalid_place_in_col_already_has_number(self):
        self.assertFalse(self.bf.is_valid_place([[1, 0, 0],
                                                 [0, 0, 0],
                                                 [0, 0, 0]], 2, 0, 1))

    def test_invalid_place_in_square_already_has_number(self):
        self.assertFalse(self.bf.is_valid_place([[1, 0, 0],
                                                 [0, 0, 0],
                                                 [0, 0, 0]], 2, 1, 1))
        self.assertFalse(self.bf.is_valid_place([[0, 0, 0, 0, 0, 0],
                                                 [0, 0, 0, 0, 0, 0],
                                                 [0, 0, 0, 0, 1, 0]], 0, 5, 1))
        board = [[0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.assertFalse(self.bf.is_valid_place(board, 1, 8, 1))
        board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.assertFalse(self.bf.is_valid_place(board, 5, 8, 1))
        board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.assertFalse(self.bf.is_valid_place(board, 7, 8, 1))

    def test_valid_place_in_square(self):
        board = [[1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.assertTrue(self.bf.is_valid_place(board, 3, 2, 1))
        board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.assertTrue(self.bf.is_valid_place(board, 4, 4, 1))

    def test_easy_board_has_15_solution_steps(self):
        game: GameBoard = self.bf.generate_board(Difficulty.EASY)
        self.assertEquals(15, len(game.get_moves()))

    def test_using_solution_solves_board(self):
        game: GameBoard = self.bf.generate_board(Difficulty.EASY)
        steps = game.get_moves()
        for (x, y, num) in steps:
            game.guess(x, y, num)

        self.assertTrue(game.is_solved())
        self.assertTrue(self.is_valid(game.get_board()))

    def is_valid(self, board):
        if self.__contains_invalid_row(board):
            return False
        if self.__contains_invalid_column(board):
            return False
        if self.__contains_invalid_square(board):
            return False

        return True

    def __contains_invalid_row(self, board):
        for row in board:
            numbers = set([])
            for val in row:
                if val in numbers:
                    return True
                else:
                    if val != 0:
                        numbers.add(val)

    def __contains_invalid_column(self, board):
        for col in range(len(board[0])):
            numbers = set([])
            for row in range(len(board)):
                if board[row][col] in numbers:
                    return True
                else:
                    if board[row][col] != 0:
                        numbers.add(board[row][col])

    def __contains_invalid_square(self, board):
        return self.__invalid_square(board, 0, 0, 2, 2)

    def __invalid_square(self, board, start_row: int, start_col: int, end_row: int, end_col: int) -> bool:
        if end_row > len(board) or end_col > len(board[0]):
            return False

        numbers = set([])
        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                if board[row][col] in numbers:
                    return True
                else:
                    if board[row][col] != 0:
                        numbers.add(board[row][col])

        if not self.__invalid_square(board, start_row, start_col + 3, end_row, end_col + 3):
            return self.__invalid_square(board, start_row + 3, 0, end_row + 3, 2)
        else:
            return True

    def create_msg(self, board: list[list[int]]) -> str:
        msg: str = "Board should be valid but was\n"
        for row in board:
            msg += "[" + ", ".join(map(str, row)) + "]\n"
        return msg
