from main.BoardFactory import Difficulty
from main.GameBoard import Position
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
        self.__current_selection: [Position] = []

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
        self.__highlight_new_selection(row, col, num)

    def __unhighlight_selection(self):
        self.__view.deactivate(self.__current_row, self.__current_col)
        for pos in self.__current_selection:
            self.__view.unhighlight(pos.row, pos.col)

    def __highlight_new_selection(self, row: int, col: int, num: int):
        self.__view.activate(row, col)
        selection = self.__game.get_selection(row, col, num)
        for pos in selection:
            self.__view.highlight(pos.row, pos.col)

        self.__current_selection = selection
        self.__current_row = row
        self.__current_col = col

