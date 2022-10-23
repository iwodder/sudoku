from copy import deepcopy


class IllegalMoveError(Exception):
    pass


class GameBoard:
    __game_board: list[list[int]]
    __solution_steps: set[(int, int, int)]

    def __init__(self, board: list[list[int]], solution: set[(int, int, int)]):
        self.__game_board = board
        self.__solution_steps = solution

    def guess(self, row: int, col: int, num: int) -> bool:
        if self.__is_inside_board(col, row):
            return self.__process_move(col, num, row)
        else:
            raise IllegalMoveError("Move must be inside the board, 0 < row < 8 and 0 < col < 8")

    def __process_move(self, col, num, row):
        if (row, col, num) in self.__solution_steps:
            self.__game_board[row][col] = num
            self.__solution_steps.remove((row, col, num))
            return True
        else:
            return False

    def __is_inside_board(self, col, row) -> bool:
        return 0 <= row <= 8 and 0 <= col <= 8

    def get_board(self):
        return self.__game_board

    def get_moves(self):
        return deepcopy(self.__solution_steps)

    def is_solved(self):
        return len(self.__solution_steps) == 0

    def __eq__(self, other):
        if isinstance(other, GameBoard):
            return self.__game_board == other.__game_board
        else:
            return False

