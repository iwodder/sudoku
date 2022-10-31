from __future__ import annotations

import tkinter.messagebox
from abc import ABC, abstractmethod
from tkinter import *
from tkinter import ttk

from main.BoardFactory import BoardFactoryImpl, Difficulty
from main.Sudoku import Sudoku, Guess


class Cell:
    __highlighted = False
    __frame: Frame = None
    __label: Label = None
    __presenter: SudokuPresenter = None
    __row: int
    __column: int

    def __init__(self, row: int, col: int, parent: Frame, presenter: SudokuPresenter):
        self.__row = row
        self.__column = col
        self.__presenter = presenter
        self.__add_frame(parent)
        self.__add_label()

    def __add_label(self):
        self.__label = ttk.Label(self.__frame, text=" ")
        self.__label.grid(row=self.__row, column=self.__column)
        self.__label.bind("<Button-1>", self.__click_handler)
        self.__label.bind("<Key>", self.__key_press_handler)

    def __add_frame(self, parent):
        self.__frame = ttk.Frame(parent, padding=10)
        self.__frame.grid(row=self.__row, column=self.__column, rowspan=1, columnspan=1)
        self.__frame.config(borderwidth=1, relief='sunken')
        self.__frame.bind("<Button-1>", self.__click_handler)
        self.__frame.bind("<Key>", self.__key_press_handler)

    def __key_press_handler(self, event: Event):
        char: str = event.char
        if char.isdigit() and char != "0":
            self.__label.configure(text=char)
            self.__deactivate()
            self.__presenter.guess_number(self.__row, self.__column, char)

    def __click_handler(self, event: Event):
        if not self.__highlighted:
            self.__activate()
        else:
            self.__deactivate()

    def __activate(self):
        self.__frame['style'] = 'Grid.TLabel'
        self.__label['style'] = 'Grid.TLabel'
        self.__frame.focus_set()
        self.__highlighted = True

    def __deactivate(self):
        self.__frame['style'] = 'TLabel'
        self.__label['style'] = 'TLabel'
        self.__highlighted = False

    def set_value(self, value: str):
        self.__label.configure(text=value)

    def change_red(self):
        self.__label['style'] = 'Wrong.TLabel'

    def change_green(self):
        self.__label['style'] = 'Correct.TLabel'


class SudokuViewInterface(ABC):

    @abstractmethod
    def set_grid_value(self, row: int, col: int, num: str):
        pass

    @abstractmethod
    def disable_start_button(self) -> None:
        pass

    @abstractmethod
    def set_cell_font_red(self, row: int, col: int):
        pass

    @abstractmethod
    def set_cell_font_green(self, row: int, col: int):
        pass

    @abstractmethod
    def show_acknowledge_dialog(self, title: str, msg: str):
        pass


class SudokuPresenter:
    __winner_msg = "You're a winner, congratulations!"
    __winner_title = "Winner :)"

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
        if not self.__game.guess_number(g):
            self.__view.set_cell_font_red(row, column)
        else:
            self.__view.set_cell_font_green(row, column)

        if self.__game.is_winner():
            self.__view.show_acknowledge_dialog(self.__winner_title, self.__winner_msg)


class GameBoard(SudokuViewInterface):
    __root: Tk = None
    __presenter: SudokuPresenter = None
    __cells: list[list[Cell]] = [[None for _ in range(9)] for _ in range(9)]
    __easy: Button = None
    __med: Button = None
    __hard: Button = None

    def __init__(self, root: Tk):
        self.__root = root
        self.__presenter = SudokuPresenter(self, Sudoku(BoardFactoryImpl()))
        self.__set_game_styles()
        self.__setup_game_board()

    def set_grid_value(self, row: int, col: int, num: str):
        self.__cells[row][col].set_value(num)

    def disable_start_button(self) -> None:
        self.__easy['state'] = 'disabled'
        self.__med['state'] = 'disabled'
        self.__hard['state'] = 'disabled'

    def set_cell_font_red(self, row: int, col: int):
        self.__cells[row][col].change_red()

    def set_cell_font_green(self, row: int, col: int):
        self.__cells[row][col].change_green()

    def show_acknowledge_dialog(self, title: str, msg: str):
        tkinter.messagebox.showinfo(title=title, message=msg)

    def __setup_game_board(self):
        self.__root.title("Sudoku")
        mainframe = ttk.Frame(self.__root, padding="3 3 3 3")
        mainframe.grid(column=0, row=0, sticky=(N, W, S, E))
        self.__root.columnconfigure(0, weight=1)
        self.__root.rowconfigure(0, weight=1)
        self.__add_cells(mainframe)
        self.__add_start_buttons(mainframe)

    def __add_cells(self, mainframe: Frame):
        for row in range(9):
            for col in range(9):
                self.__cells[row][col] = Cell(row, col, mainframe, self.__presenter)

    def __add_start_buttons(self, frame: Frame):
        self.__easy = ttk.Button(frame, text="Easy", command=lambda: self.__presenter.start_new_game(Difficulty.EASY))
        self.__easy.grid(row=10, column=0, rowspan=1, columnspan=3, sticky=E)
        self.__med = ttk.Button(frame, text="Medium", command=lambda: self.__presenter.start_new_game(Difficulty.MEDIUM))
        self.__med.grid(row=10, column=3, rowspan=1, columnspan=3, sticky=(E, W))
        self.__hard = ttk.Button(frame, text="Hard", command=lambda: self.__presenter.start_new_game(Difficulty.HARD))
        self.__hard.grid(row=10, column=6, rowspan=1, columnspan=3, sticky=W)

    def __set_game_styles(self):
        style = ttk.Style()
        style.configure('Grid.TLabel', background='#ccffff')
        style.configure('Wrong.TLabel', foreground='#ff0000')
        style.configure('Correct.TLabel', foreground='#00cc00')

    def run(self):
        self.__root.mainloop()
