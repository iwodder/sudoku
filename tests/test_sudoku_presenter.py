import unittest

from main.BoardFactory import Difficulty
from main.GuiRunner import SudokuPresenter, SudokuViewInterface
from main.Sudoku import Sudoku
from tests.test_sudoku import StubbedBoardFactory


class TestSudokuPresenter(unittest.TestCase, SudokuViewInterface):
    __start_disabled: bool = False
    __prompted: bool = False
    __set_red: bool = False
    __set_green: bool = False
    __msg: str = ""
    __title: str = ""
    moves: [(int, int, str)] = []

    def set_grid_value(self, row: int, col: int, num: str):
        self.moves.append((row, col, num))

    def disable_start_button(self) -> None:
        self.__start_disabled = not self.__start_disabled

    def set_cell_font_red(self, row: int, col: int):
        self.__set_red = True

    def set_cell_font_green(self, row: int, col: int):
        self.__set_green = True

    def show_acknowledge_dialog(self, title: str, msg: str):
        self.__msg = msg
        self.__title = title

    def setUp(self) -> None:
        self.moves = []
        self.__start_disabled = False

    def test_presenter(self):
        pres = SudokuPresenter(self, Sudoku(StubbedBoardFactory()))

    def test_start_new_game_disables_start_menu(self):
        pres = SudokuPresenter(self, Sudoku(StubbedBoardFactory()))
        pres.start_new_game(Difficulty.EASY)
        self.assertTrue(self.__start_disabled)

    def test_start_new_game_sets_cell_values(self):
        pres = SudokuPresenter(self, Sudoku(StubbedBoardFactory()))
        pres.start_new_game(Difficulty.EASY)
        self.assertTrue(len(self.moves) > 0)

    def test_start_new_game_sets_all_cell_values(self):
        pres = SudokuPresenter(self, Sudoku(StubbedBoardFactory()))
        pres.start_new_game(Difficulty.EASY)
        self.assertEqual(81, len(self.moves))

    def test_guess_number_incorrect_changes_cell_to_red(self):
        pres = SudokuPresenter(self, Sudoku(StubbedBoardFactory()))
        pres.start_new_game(Difficulty.OFF)

        pres.guess_number(0, 1, "9")

        self.assertTrue(self.__set_red)

    def test_guess_number_correct_changes_cell_to_green(self):
        pres = SudokuPresenter(self, Sudoku(StubbedBoardFactory()))
        pres.start_new_game(Difficulty.OFF)

        pres.guess_number(0, 0, "9")

        self.assertTrue(self.__set_green)

    def test_correct_guess_for_last_number_prints_winner_dialog(self):
        pres = SudokuPresenter(self, Sudoku(StubbedBoardFactory()))
        pres.start_new_game(Difficulty.OFF)

        pres.guess_number(0, 0, "9")
        pres.guess_number(7, 7, "1")

        self.assertEqual(self.__msg, "You're a winner, congratulations!")
        self.assertEqual(self.__title, "Winner :)")
