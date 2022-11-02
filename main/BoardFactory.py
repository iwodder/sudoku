from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from random import shuffle, random
from .GameBoard import GameBoard


class Difficulty(Enum):
    OFF = 0
    EASY = 15
    MEDIUM = 25
    HARD = 35

    def empty_squares(self) -> int:
        return self.value


class BoardFactory(ABC):

    @abstractmethod
    def generate_board(self, difficulty: Difficulty) -> GameBoard:
        pass


class BoardFactoryImpl(BoardFactory):
    __size = 9

    def generate_board(self, difficulty: Difficulty) -> GameBoard:
        board = [[0 for x in range(self.__size)] for x in range(self.__size)]
        self.__fill_board(board)
        return GameBoard(board, self.__generate_solution(board, difficulty))

    def place_number(self, board, num, col: int = 0) -> bool:
        if col >= len(board):
            return True

        for row in range(len(board)):
            if self.is_valid_place(board, row, col, num):
                board[row][col] = num
                if self.place_number(board, num, col + 1):
                    return True

                board[row][col] = 0

        return False

    def __fill_board(self, board):
        vals: list[int] = [x for x in range(1, 10)]
        shuffle(vals)
        for num in vals:
            self.place_number(board, num)

    def __generate_solution(self, board, difficulty):
        solution_steps = set([])
        while len(solution_steps) < difficulty.empty_squares():
            (x, y) = int(random() * 8), int(random() * 8)
            val = board[x][y]
            solution_steps.add((x, y, val))

        for (x, y, _) in solution_steps:
            board[x][y] = 0

        return solution_steps

    def is_valid_place(self, board: list[list[int]], row: int, col: int, num: int):
        if row > (len(board) - 1) or col > (len(board[0]) - 1):
            return False
        elif board[row][col] != 0:
            return False
        elif num in set(board[row]):
            return False
        elif num in self.__get_col_numbers(board, col):
            return False
        elif num in self.__get_sub_square_numbers(board, row, col):
            return False
        else:
            return True

    def __get_sub_square(self, row: int, col: int) -> (int, int):
        if row < 3:
            if col < 3:
                return 0, 0
            elif col < 6:
                return 0, 3
            else:
                return 0, 6
        elif row < 6:
            if col < 3:
                return 3, 0
            elif col < 6:
                return 3, 3
            else:
                return 3, 6
        else:
            if col < 3:
                return 6, 0
            elif col < 6:
                return 6, 3
            else:
                return 6, 6

    def __get_col_numbers(self, board, col) -> set[int]:
        col_nums = set([])
        for b_row in board:
            col_nums.add(b_row[col])

        return col_nums

    def __get_sub_square_numbers(self, board, row, col) -> set[int]:
        start_row, start_col = self.__get_sub_square(row, col)
        square_nums = set([])
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                square_nums.add(board[i][j])

        return square_nums
