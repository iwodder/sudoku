import unittest

from main.BoardFactory import Difficulty
from main.gui.GuiRunner import SudokuPresenter, SudokuViewInterface
from main.Sudoku import Sudoku
from tests.test_sudoku import StubbedBoardFactory


class TestSudokuPresenter(unittest.TestCase, SudokuViewInterface):
    __start_disabled: bool = False
    __prompted: bool = False
    __color: str = ""
    __msg: str = ""
    __title: str = ""
    __active_cell = None
    __last_deactivated = False
    __highlights = None
    __unhighlights = None
    moves: [(int, int, str)] = []

    def set_grid_value(self, row: int, col: int, num: str):
        self.moves.append((row, col, num))

    def disable_start_button(self) -> None:
        self.__start_disabled = not self.__start_disabled

    def show_acknowledge_dialog(self, title: str, msg: str):
        self.__msg = msg
        self.__title = title

    def activate(self, row: int, col: int):
        self.__active_cell = (row, col)

    def set_cell_font_color(self, row: int, col: int, color: str):
        self.__color = color

    def deactivate(self, row: int, col: int):
        self.__last_deactivated = (row, col)

    def highlight(self, row: int, col: int):
        self.__highlights.add((row, col))

    def unhighlight(self, row: int, col: int):
        self.__unhighlights.add((row, col))

    def setUp(self) -> None:
        self.moves = []
        self.__start_disabled = False
        self.__highlights = set([])
        self.__unhighlights = set([])

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

        self.assertEqual("#ff0000", self.__color)

    def test_guess_number_correct_changes_cell_to_green(self):
        pres = SudokuPresenter(self, Sudoku(StubbedBoardFactory()))
        pres.start_new_game(Difficulty.OFF)

        pres.guess_number(0, 0, "9")

        self.assertEqual("#00cc00", self.__color)

    def test_correct_guess_for_last_number_prints_winner_dialog(self):
        pres = SudokuPresenter(self, Sudoku(StubbedBoardFactory()))
        pres.start_new_game(Difficulty.OFF)

        pres.guess_number(0, 0, "9")
        pres.guess_number(7, 7, "1")

        self.assertEqual(self.__msg, "You're a winner, congratulations!")
        self.assertEqual(self.__title, "Winner :)")

    def test_guessing_number_deactivates_cell(self):
        pres = SudokuPresenter(self, Sudoku(StubbedBoardFactory()))
        pres.start_new_game(Difficulty.OFF)

        pres.guess_number(0, 0, "9")

        self.assertTrue(self.__last_deactivated)

    def test_choosing_cell_sets_active_cell_and_deactivates_old(self):
        pres = SudokuPresenter(self, Sudoku(StubbedBoardFactory()))

        pres.select(0, 0)
        pres.select(0, 2)

        self.assertEqual((0, 2), self.__active_cell)
        self.assertEqual((0, 0), self.__last_deactivated)

    def test_choosing_cell_highlights_row_and_col_except_selected_cell(self):
        pres = SudokuPresenter(self, Sudoku(StubbedBoardFactory()))

        pres.select(0, 0)

        self.assertEqual(16, len(self.__highlights))
        self.__row_was_highlighted(0, 0)
        self.__col_was_highlighted(0, 0)

    def test_choosing_cell_unhighlights_previous_row_and_col_except_selected_cell(self):
        pres = SudokuPresenter(self, Sudoku(StubbedBoardFactory()))

        pres.select(1, 2)
        pres.select(0, 0)

        self.assertEqual(16, len(self.__unhighlights))
        self.__row_was_unhighlighted(2, 1)
        self.__col_was_unhighlighted(1, 2)

    def __row_was_highlighted(self, col_exclude: int, row: int):
        for col in range(9):
            if col != col_exclude and (row, col) not in self.__highlights:
                self.fail(f"Expected to find (row={row}, col={col})")

    def __col_was_highlighted(self, row_exclude: int, col: int):
        for row in range(9):
            if row != row_exclude and (row, col) not in self.__highlights:
                self.fail(f"Expected to find (row={row}, col={col})")

    def __row_was_unhighlighted(self, col_exclude: int, row: int):
        for col in range(9):
            if col != col_exclude and (row, col) not in self.__unhighlights:
                self.fail(f"Expected to find (row={row}, col={col})")

    def __col_was_unhighlighted(self, row_exclude: int, col: int):
        for row in range(9):
            if row != row_exclude and (row, col) not in self.__unhighlights:
                self.fail(f"Expected to find (row={row}, col={col})")

