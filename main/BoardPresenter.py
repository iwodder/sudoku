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
    __current_num = -1

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

    def select(self, row: int, col: int, num: int = 0):
        self.__unhighlight_selection()
        self.__current_row = row
        self.__current_col = col
        if num != 0:
            self.__current_num = num
        self.__highlight_new_selection()

    def __unhighlight_selection(self):
        self.__view.deactivate(self.__current_row, self.__current_col)
        self.__modify_row(self.__view.unhighlight)
        self.__modify_col(self.__view.unhighlight)
        self.__modify_square(self.__view.unhighlight)
        self.__modify_number(self.__view.unhighlight)

    def __highlight_new_selection(self):
        self.__view.activate(self.__current_row, self.__current_col)
        self.__modify_row(self.__view.highlight)
        self.__modify_col(self.__view.highlight)
        self.__modify_square(self.__view.highlight)
        self.__modify_number(self.__view.highlight)

    def __modify_number(self, action):
        if self.__current_num > -1:
            locations = self.__game.get_all_locations_of(self.__current_num)
            for (row, col) in locations:
                if row != self.__current_row and col != self.__current_col:
                    action(row, col)

    def __modify_row(self, action):
        if self.__current_row != -1:
            for col in range(9):
                if col != self.__current_col:
                    action(self.__current_row, col)

    def __modify_col(self, action):
        if self.__current_col != -1:
            for row in range(9):
                if row != self.__current_row:
                    action(row, self.__current_col)

    def __modify_square(self, action):
        if self.__current_col > -1 and self.__current_row > -1:
            starting_col = self.__get_starting(self.__current_col)
            starting_row = self.__get_starting(self.__current_row)
            for x in range(starting_row, starting_row + 3):
                for y in range(starting_col, starting_col + 3):
                    if x != self.__current_row and y != self.__current_col:
                        action(x, y)

    def __get_starting(self, num: int) -> int:
        if 0 <= num <= 2:
            return 0
        elif num <= 5:
            return 3
        else:
            return 6
