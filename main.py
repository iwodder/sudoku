from main.BoardFactory import BoardFactoryImpl
from main.CliRunner import CliRunner
from main.gui.GuiRunner import GameBoard
from main.Sudoku import Sudoku
from tkinter import *
from sys import argv

if __name__ == '__main__':
    if len(argv) < 2:
        print("Must specify type")
        print("\t--cli or --gui")
    else:
        if argv[1] == "--cli":
            cli: CliRunner = CliRunner(Sudoku(BoardFactoryImpl()))
            cli.run()
        elif argv[1] == "--gui":
            game = GameBoard(Tk())
            game.run()
