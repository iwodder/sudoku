from __future__ import annotations

from dataclasses import dataclass
from main.BoardFactory import BoardFactory, Difficulty
from main.GameBoard import GameBoard, Position


class Sudoku:
    __started: bool = False
    __board_factory: BoardFactory = None
    __user_board: GameBoard = None
    __wrong_guesses: [Guess]
    __right_guesses: [Guess]

    def __init__(self, board_factory: BoardFactory):
        self.__board_factory = board_factory
        self.__right_guesses = []
        self.__wrong_guesses = []

    def game_started(self) -> bool:
        return self.__started

    def guess_number(self, guess: Guess):
        if guess in self.__right_guesses:
            return True
        elif guess in self.__wrong_guesses:
            return False
        else:
            return self.__process_new_guess(guess)

    def __process_new_guess(self, guess):
        if self.__user_board.guess(guess.row, guess.col, guess.number):
            self.__right_guesses.append(guess)
            return True
        else:
            self.__wrong_guesses.append(guess)
            return False

    def is_winner(self) -> bool:
        self.__started = False
        return self.__user_board.is_solved() and len(self.__wrong_guesses) < 3

    def game_over(self):
        return len(self.__wrong_guesses) == 3 or self.__user_board.is_solved()

    def get_user_board(self) -> list[list[int]]:
        return self.__user_board.get_board()

    def get_selection(self, row: int, col: int, num: int) -> list[Position]:
        return self.__user_board.get_selection(row, col, num)

    def __str__(self):
        return BoardFormatter(self.__user_board.get_board()).format()

    def start_new_game(self, difficulty: Difficulty):
        self.__user_board = self.__board_factory.generate_board(difficulty)
        self.__started = True

    def get_values(self):
        return self.__user_board.get_values()



@dataclass(frozen=True)
class Guess:
    row: int = 0
    col: int = 0
    number: int = 0


class BoardFormatter:
    __header_footer = "=======================================\n"
    __row_format = "| {0} | {1} | {2} || {3} | {4} | {5} || {6} | {7} | {8} |\n"
    __cell_separator = "============||===========||============\n"

    def __init__(self, board: list[list[int]]):
        self.__board = board

    def format(self):
        result: str = self.__header_footer

        row_cnt: int = 0
        for row in self.__board:
            result += self.__row_format.format(*[self.__convert_to_str(x) for x in row])
            if self.__should_add_separator(row_cnt):
                result += self.__cell_separator
            row_cnt += 1

        result += self.__header_footer
        return result

    def __should_add_separator(self, row_cnt):
        return row_cnt == 2 or row_cnt == 5

    def __convert_to_str(self, x: int) -> str:
        if x == 0:
            return ' '
        else:
            return str(x)
