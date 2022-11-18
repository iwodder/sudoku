from __future__ import annotations

import tkinter.messagebox
from tkinter import *
from tkinter import ttk

from main.BoardFactory import BoardFactoryImpl, Difficulty
from main.Sudoku import Sudoku
from main.BoardPresenter import SudokuPresenter
from main.gui.Cell import Cell
from main.gui.SudokuViewInterface import SudokuViewInterface


class GameBoard(SudokuViewInterface):
    __root: Tk = None
    __presenter: SudokuPresenter = None
    __cells: list[list[Cell]] = [[None for _ in range(9)] for _ in range(9)]
    __active_cell_row: int = None
    __active_cell_col: int = None
    __easy: Button = None
    __med: Button = None
    __hard: Button = None

    def __init__(self, root: Tk):
        self.__root = root
        self.__root.option_add('*tearOff', FALSE)
        self.__presenter = SudokuPresenter(self, Sudoku(BoardFactoryImpl()))
        self.__set_game_styles()
        self.__setup_game_board()

    def set_grid_value(self, row: int, col: int, num: str):
        self.__cells[row][col].set_value(num)

    def disable_start_button(self) -> None:
        self.__easy['state'] = 'disabled'
        self.__med['state'] = 'disabled'
        self.__hard['state'] = 'disabled'

    def set_cell_font_color(self, row: int, col: int, color: str):
        self.__cells[row][col].change_font_color(color)

    def show_acknowledge_dialog(self, title: str, msg: str):
        tkinter.messagebox.showinfo(title=title, message=msg)

    def activate(self, row: int, col: int):
        if 0 <= row <= 8 and 0 <= col <= 8:
            self.__cells[row][col].select()

    def deactivate(self, row: int, col: int):
        if 0 <= row <= 8 and 0 <= col <= 8:
            self.__cells[row][col].deselect()

    def highlight(self, row: int, col: int):
        if 0 <= row <= 8 and 0 <= col <= 8:
            self.__cells[row][col].highlight()

    def unhighlight(self, row: int, col: int):
        if 0 <= row <= 8 and 0 <= col <= 8:
            self.__cells[row][col].unhighlight()

    def enable_end_game_button(self) -> None:
        self.__file_menu.entryconfigure("End Game", state=ACTIVE)

    def enable_start_button(self) -> None:
        self.__easy['state'] = 'active'
        self.__med['state'] = 'active'
        self.__hard['state'] = 'active'

    def disable_end_game_button(self) -> None:
        self.__file_menu.entryconfigure("End Game", state=DISABLED)

    def __setup_game_board(self):
        self.__root.title("Sudoku")
        mainframe = ttk.Frame(self.__root)
        mainframe.grid(column=0, row=0, pady=5, padx=5)

        menu_bar = Menu(self.__root)
        self.__file_menu = Menu(menu_bar)
        menu_bar.add_cascade(menu=self.__file_menu, label="File")
        self.__file_menu.add_command(label="End Game", command=self.__presenter.end_game)
        self.__root.configure(menu=menu_bar)

        cell_frame = ttk.Frame(mainframe)
        cell_frame.grid(column=0, row=0, columnspan=1, rowspan=1, padx=5, pady=5)
        self.__add_start_buttons(mainframe)
        self.__add_cells(cell_frame)
        self.disable_end_game_button()

    def __add_cells(self, mainframe: Frame):
        for row in range(9):
            for col in range(9):
                self.__cells[row][col] = Cell(row, col, mainframe, self.__presenter)

    def __add_start_buttons(self, frame: Frame):
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=3, rowspan=2)
        self.__easy = ttk.Button(button_frame, text="Easy", style='Difficulty.TButton',
                                 command=lambda: self.__presenter.start_new_game(Difficulty.EASY))
        self.__easy.grid(row=1, column=0, rowspan=2, columnspan=6, sticky=E)
        self.__med = ttk.Button(button_frame, text="Medium", style='Difficulty.TButton',
                                command=lambda: self.__presenter.start_new_game(Difficulty.MEDIUM))
        self.__med.grid(row=1, column=6, rowspan=2, columnspan=6, sticky=(E, W))
        self.__hard = ttk.Button(button_frame, text="Hard", style='Difficulty.TButton',
                                 command=lambda: self.__presenter.start_new_game(Difficulty.HARD))
        self.__hard.grid(row=1, column=12, rowspan=2, columnspan=6, sticky=W)

    def __set_game_styles(self):
        style = ttk.Style()
        style.configure('Selected.TLabel', background='#ccffff')
        style.configure('Highlight.TLabel', background='#848788')
        style.configure('Difficulty.TButton', font="Times 16")

    def run(self):
        self.__root.mainloop()
