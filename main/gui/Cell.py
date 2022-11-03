from tkinter import *
from tkinter import ttk
from main.BoardPresenter import SudokuPresenter


class Cell:
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
            self.__presenter.guess_number(self.__row, self.__column, char)

    def __click_handler(self, event: Event):
        num = 0
        if self.__label.cget("text").isdecimal():
            num = int(self.__label.cget("text"))

        self.__presenter.select(self.__row, self.__column, num)

    def select(self):
        self.__frame['style'] = 'Selected.TLabel'
        self.__label['style'] = 'Selected.TLabel'
        self.__frame.focus_set()

    def deselect(self):
        self.__frame['style'] = 'TLabel'
        self.__label['style'] = 'TLabel'

    def set_value(self, value: str):
        self.__label.configure(text=value)

    def change_font_color(self, color: str):
        self.__label.configure(foreground=color)

    def highlight(self):
        self.__frame['style'] = 'Highlight.TLabel'
        self.__label['style'] = 'Highlight.TLabel'

    def unhighlight(self):
        self.__frame['style'] = 'TLabel'
        self.__label['style'] = 'TLabel'

