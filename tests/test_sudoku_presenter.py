import unittest

from main.BoardFactory import Difficulty
from main.gui.GuiRunner import SudokuPresenter, SudokuViewInterface
from main.Sudoku import Sudoku
from tests.test_sudoku import StubbedBoardFactory


class SpySudokuInterface(SudokuViewInterface):

    def __init__(self):
        self.start_disabled: bool = False
        self.prompted: bool = False
        self.color: str = ""
        self.msg: str = ""
        self.title: str = ""
        self.active_cell = None
        self.last_deactivated = False
        self.highlights = set([])
        self.unhighlights = set([])
        self.end_game_enabled = False
        self.moves: [(int, int, str)] = []

    def set_grid_value(self, row: int, col: int, num: str):
        self.moves.append((row, col, num))

    def disable_start_button(self) -> None:
        self.start_disabled = not self.start_disabled

    def show_acknowledge_dialog(self, title: str, msg: str):
        self.msg = msg
        self.title = title

    def activate(self, row: int, col: int):
        self.active_cell = (row, col)

    def set_cell_font_color(self, row: int, col: int, color: str):
        self.color = color

    def deactivate(self, row: int, col: int):
        self.last_deactivated = (row, col)

    def highlight(self, row: int, col: int):
        self.highlights.add((row, col))

    def unhighlight(self, row: int, col: int):
        self.unhighlights.add((row, col))

    def enable_end_game_button(self) -> None:
        self.end_game_enabled = True

    def enable_start_button(self) -> None:
        self.start_disabled = False

    def disable_end_game_button(self) -> None:
        self.end_game_enabled = False


class TestSudokuPresenter(unittest.TestCase):

    def setUp(self) -> None:
        self.view_spy = SpySudokuInterface()
        self.presenter = SudokuPresenter(self.view_spy, Sudoku(StubbedBoardFactory()))
        self.presenter.start_new_game(Difficulty.EASY)

    def test_start_new_game_disables_start_menu(self):
        self.assertTrue(self.view_spy.start_disabled)

    def test_start_new_game_sets_cell_values(self):
        self.assertTrue(len(self.view_spy.moves) > 0)

    def test_start_new_game_sets_all_cell_values(self):
        self.assertEqual(81, len(self.view_spy.moves))

    def test_starting_new_game_twice_displays_dialog_to_end_game(self):
        self.presenter.start_new_game(Difficulty.EASY)

        self.assertEqual(self.view_spy.msg, "Please end current game to start a new one.")
        self.assertEqual(self.view_spy.title, "Info")

    def test_starting_new_game_enables_end_game_button(self):
        self.assertTrue(self.view_spy.end_game_enabled)

    def test_guess_number_incorrect_changes_cell_to_red(self):
        self.presenter.guess_number(0, 1, "9")

        self.assertEqual("#ff0000", self.view_spy.color)

    def test_guess_number_correct_changes_cell_to_green(self):
        self.presenter.guess_number(0, 0, "9")

        self.assertEqual("#00cc00", self.view_spy.color)

    def test_correct_guess_for_last_number_prints_winner_dialog(self):
        self.presenter.guess_number(0, 0, "9")
        self.presenter.guess_number(7, 7, "1")

        self.assertEqual(self.view_spy.msg, "You're a winner, congratulations!")
        self.assertEqual(self.view_spy.title, "Winner :)")

    def test_guessing_number_deactivates_cell(self):
        self.presenter.guess_number(0, 0, "9")

        self.assertTrue(self.view_spy.last_deactivated)

    def test_choosing_cell_sets_active_cell_and_deactivates_old(self):
        self.presenter.select(0, 0)
        self.presenter.select(0, 2)

        self.assertEqual((0, 2), self.view_spy.active_cell)
        self.assertEqual((0, 0), self.view_spy.last_deactivated)

    def test_choosing_cell_highlights_row_and_col_except_selected_cell(self):
        self.presenter.select(0, 0)

        self.__row_was_highlighted(0, 0)
        self.__col_was_highlighted(0, 0)

    def test_choosing_cell_unhighlights_previous_row_and_col_except_selected_cell(self):
        self.presenter.select(1, 2)
        self.presenter.select(0, 0)

        self.__row_was_unhighlighted(2, 1)
        self.__col_was_unhighlighted(1, 2)

    def test_choosing_cell_highlights_square_of_selected_cell(self):
        self.presenter.select(1, 2)

        self.__square_was_modified(1, 2, self.view_spy.highlights)

    def test_choosing_cell_unhighlights_previous_square_of_selected_cell(self):
        self.presenter.select(1, 2)
        self.presenter.select(0, 0)

        self.__square_was_modified(1, 2, self.view_spy.unhighlights)

    def test_highlights_all_numbers_if_selected_cell_has_number(self):
        self.presenter.select(1, 2, 6)

        expected_values = {(0, 1), (1, 4), (2, 7), (3, 2), (4, 5), (5, 8), (6, 0), (7, 3), (8, 6)}
        for (row, col) in expected_values:
            self.assertTrue((row, col) in self.view_spy.highlights)

        self.assertFalse((1, 2) in self.view_spy.highlights)

    def test_unhighlights_last_number_when_new_number_selected_cell(self):
        self.presenter.select(1, 2, 6)
        self.presenter.select(1, 2, 9)

        expected_values = {(0, 1), (1, 4), (2, 7), (3, 2), (4, 5), (5, 8), (6, 0), (7, 3), (8, 6)}
        for (row, col) in expected_values:
            self.assertTrue((row, col) in self.view_spy.unhighlights)

    def test_shouldnt_highlight_number_when_zero(self):
        self.presenter.select(3, 3, 0)

        unexpected_values = {(0, 0), (7, 7)}
        for (row, col) in unexpected_values:
            self.assertFalse((row, col) in self.view_spy.highlights)

    def test_three_different_incorrect_guesses_prints_loser_dialog(self):
        self.presenter.guess_number(0, 0, "8")
        self.presenter.guess_number(7, 7, "8")
        self.presenter.guess_number(1, 1, "8")

        self.assertEqual(self.view_spy.msg, "You lose.")
        self.assertEqual(self.view_spy.title, "Loser :(")

    def test_ending_game_enables_start_buttons_and_disables_end_game(self):
        self.presenter.end_game()

        self.assertFalse(self.view_spy.end_game_enabled)
        self.assertFalse(self.view_spy.start_disabled)

    def test_ending_game_clears_board(self):
        self.view_spy.moves.clear()
        self.presenter.end_game()

        self.assertEqual(81, len(self.view_spy.moves))
        self.assertEqual(0, len(list(filter(lambda move: move[2] != " ", self.view_spy.moves))))

    def __row_was_highlighted(self, col_exclude: int, row: int):
        for col in range(9):
            if col != col_exclude and (row, col) not in self.view_spy.highlights:
                self.fail(f"Expected to find (row={row}, col={col})")

    def __col_was_highlighted(self, row_exclude: int, col: int):
        for row in range(9):
            if row != row_exclude and (row, col) not in self.view_spy.highlights:
                self.fail(f"Expected to find (row={row}, col={col})")

    def __square_was_modified(self, row: int, col: int, moves):
        starting_row = self.__get_starting(row)
        starting_col = self.__get_starting(col)
        for x in range(starting_row, starting_row + 3):
            for y in range(starting_col, starting_col + 3):
                if x != row and y != col:
                    if (x, y) not in moves:
                        self.fail(f"Expected to find (row={x}, col={y}), but only had {moves})")

    def __row_was_unhighlighted(self, col_exclude: int, row: int):
        for col in range(9):
            if col != col_exclude and (row, col) not in self.view_spy.unhighlights:
                self.fail(f"Expected to find (row={row}, col={col})")

    def __col_was_unhighlighted(self, row_exclude: int, col: int):
        for row in range(9):
            if row != row_exclude and (row, col) not in self.view_spy.unhighlights:
                self.fail(f"Expected to find (row={row}, col={col})")

    def __get_starting(self, num: int) -> int:
        if 0 <= num <= 2:
            return 0
        elif num <= 5:
            return 3
        else:
            return 6
