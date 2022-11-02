from main.BoardFactory import Difficulty
from main.gui.SudokuViewInterface import SudokuViewInterface
from main.Sudoku import Sudoku, Guess


class SudokuPresenter:
    __winner_msg = "You're a winner, congratulations!"
    __winner_title = "Winner :)"
    __red_color = '#ff0000'
    __green_color = '#00cc00'
    __current_row = -1
    __current_col = -1

    def __init__(self, view: SudokuViewInterface, sudoku_game: Sudoku):
        self.__view = view
        self.__game = sudoku_game

    def start_new_game(self, difficulty: Difficulty):
        self.__game.start_new_game(difficulty)
        self.__view.disable_start_button()

        for row in range(len(self.__game.get_user_board())):
            for col in range(len(self.__game.get_user_board()[row])):
                num = self.__game.get_user_board()[row][col]
                if num == 0:
                    num = ' '
                self.__view.set_grid_value(row, col, str(num))

    def guess_number(self, row: int, column: int, number: str):
        g = Guess(row, column, int(number))
        self.__view.deactivate(self.__current_row, self.__current_col)

        if not self.__game.guess_number(g):
            self.__view.set_cell_font_color(row, column, self.__red_color)
        else:
            self.__view.set_cell_font_color(row, column, self.__green_color)

        if self.__game.is_winner():
            self.__view.show_acknowledge_dialog(self.__winner_title, self.__winner_msg)

    def select(self, row: int, col: int):
        self.__view.deactivate(self.__current_row, self.__current_col)
        self.__unhighlight_row()
        self.__unhighlight_col()
        self.__unhighlight_square()
        self.__current_row = row
        self.__current_col = col
        self.__view.activate(self.__current_row, self.__current_col)
        self.__highlight_row()
        self.__highlight_col()
        self.__highlight_square()

    def __highlight_row(self):
        for col in range(9):
            if col != self.__current_col:
                self.__view.highlight(self.__current_row, col)

    def __highlight_col(self):
        for row in range(9):
            if row != self.__current_row:
                self.__view.highlight(row, self.__current_col)

    def __unhighlight_row(self):
        if self.__current_row != -1:
            for col in range(9):
                if col != self.__current_col:
                    self.__view.unhighlight(self.__current_row, col)

    def __unhighlight_col(self):
        if self.__current_col != -1:
            for row in range(9):
                if row != self.__current_row:
                    self.__view.unhighlight(row, self.__current_col)

    def __highlight_square(self):
        starting_col = self.__get_starting(self.__current_col)
        starting_row = self.__get_starting(self.__current_row)
        for x in range(starting_row, starting_row + 3):
            for y in range(starting_col, starting_col + 3):
                if self.__current_row != x and self.__current_col != y:
                    self.__view.highlight(x, y)

    def __unhighlight_square(self):
        if self.__current_col > -1 and self.__current_row > -1:
            starting_col = self.__get_starting(self.__current_col)
            starting_row = self.__get_starting(self.__current_row)
            for x in range(starting_row, starting_row + 3):
                for y in range(starting_col, starting_col + 3):
                    self.__view.unhighlight(x, y)

    def __get_starting(self, num: int) -> int:
        if 0 <= num <= 2:
            return 0
        elif num <= 5:
            return 3
        else:
            return 6
