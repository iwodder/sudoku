from main.BoardFactory import Difficulty
from main.GameBoard import Position
from main.gui.SudokuViewInterface import SudokuViewInterface
from main.Sudoku import Sudoku, Guess, IllegalStateException


class SudokuPresenter:
    __winner_msg = "You're a winner, congratulations!"
    __winner_title = "Winner :)"
    __loser_msg = "You lose."
    __loser_title = "Loser :("
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
        try:
            self.__game.start_new_game(difficulty)
            self.__view.disable_start_button()
            self.__view.enable_end_game_button()

            for val in self.__game.get_values():
                self.__view.set_grid_value(val.row, val.col, val.value)

        except IllegalStateException:
            self.__view.show_acknowledge_dialog("Info", "Please end current game to start a new one.")

    def guess_number(self, row: int, column: int, number: str):
        g = Guess(row, column, int(number))
        self.__view.deactivate(self.__current_row, self.__current_col)

        if self.__game.guess_number(g):
            self.__view.set_cell_font_color(row, column, self.__green_color)
        else:
            self.__view.set_cell_font_color(row, column, self.__red_color)

        if self.__game.game_over():
            if self.__game.is_winner():
                self.__view.show_acknowledge_dialog(self.__winner_title, self.__winner_msg)
            else:
                self.__view.show_acknowledge_dialog(self.__loser_title, self.__loser_msg)
            self.end_game()

    def select(self, row: int, col: int, num: int = 0):
        self.__unhighlight_selection()
        self.__highlight_new_selection(row, col, num)

    def end_game(self):
        self.__game.end_game()
        for x in range(9):
            for y in range(9):
                self.__view.set_grid_value(x, y, " ")

        self.__view.disable_end_game_button()
        self.__view.enable_start_button()

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

