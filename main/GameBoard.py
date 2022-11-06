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
        for x in range(9):
            if x != col:
                result.append(Position(row, x))
            if x != row:
                result.append(Position(x, col))

        starting_col = self.__get_starting(col)
        starting_row = self.__get_starting(row)
        for x in range(starting_row, starting_row + 3):
            for y in range(starting_col, starting_col + 3):
                if x != row and y != col:
                    result.append(Position(x, y))

        self.__get_all_locations_of(num, result)

        return result

    def is_solved(self):
        return len(self.__solution_steps) == 0

    def __get_all_locations_of(self, num: int, locations: [Position]):
        if num != 0:
            for row in range(len(self.__game_board)):
                for col in range(len(self.__game_board[row])):
                    if self.__game_board[row][col] == num:
                        locations.append(Position(row, col))

        return locations

    def __get_starting(self, num: int) -> int:
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