from main.BoardFactory import BoardFactoryImpl
from main.CliRunner import CliRunner
from main.Sudoku import Sudoku

if __name__ == '__main__':
    cli: CliRunner = CliRunner(Sudoku(BoardFactoryImpl()))
    cli.run()