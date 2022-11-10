from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass


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
            raise IllegalMoveError("Move must be inside the board, 0 <= row <= 8 and 0 <= col <= 8")

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

    def get_selection(self, row: int, col: int, num: int) -> list[Position]:
        result = []
        self.__get_row_and_col(col, row, result)
        self.__get_square(col, row, result)
        self.__get_all_locations_of(num, result)
        return result

    def get_values(self) -> list[Value]:
        result = []
        for row in range(9):
            for col in range(9):
                value = str(self.__game_board[row][col])
                if value == '0':
                    value = ' '
                result.append(Value(row, col, value))
        return result

    def is_solved(self):
        return len(self.__solution_steps) == 0

    def __get_row_and_col(self, col: int, row: int, result: list[Position]):
        for x in range(9):
            if x != col:
                result.append(Position(row, x))
            if x != row:
                result.append(Position(x, col))

    def __get_square(self, col: int, row: int, result: list[Position]):
        starting_col = self.__get_start_value(col)
        starting_row = self.__get_start_value(row)
        for x in range(starting_row, starting_row + 3):
            for y in range(starting_col, starting_col + 3):
                if x != row and y != col:
                    result.append(Position(x, y))

    def __get_all_locations_of(self, num: int, locations: list[Position]):
        if num != 0:
            for row in range(len(self.__game_board)):
                for col in range(len(self.__game_board[row])):
                    if self.__game_board[row][col] == num:
                        locations.append(Position(row, col))

        return locations

    def __get_start_value(self, num: int) -> int:
        if 0 <= num <= 2:
            return 0
        elif num <= 5:
            return 3
        else:
            return 6

    def __eq__(self, other):
        if isinstance(other, GameBoard):
            return self.__game_board == other.__game_board
        else:
            return False


@dataclass(frozen=True)
class Position:
    row: int = -1
    col: int = -1


@dataclass(frozen=True)
class Value:
    row: int = 0
    col: int = 0
    value: str = ''
