from typing import TextIO

from main.BoardFactory import Difficulty
from main.Sudoku import Sudoku, Guess


class CliRunner:
    __difficulty_mapping = {1: Difficulty.EASY, 2: Difficulty.MEDIUM, 3: Difficulty.HARD}
    __sudoku: Sudoku = None
    __exit: bool = False

    def __init__(self, sudoku: Sudoku):
        self.__sudoku = sudoku

    def run(self):
        print("=== Welcome to Sudoku ===")
        while not self.__exit:
            choice = self.__get_user_input(self.__print_welcome_menu)
            if choice == 1:
                self.__start_new_game()
            elif choice == 2:
                print("Quitting...")
                self.__exit = True
        exit(0)

    def __start_new_game(self):
        choice = self.__get_user_input(self.__print_difficulty_menu)
        self.__sudoku.set_difficulty(self.__difficulty_mapping.get(choice))
        self.__sudoku.start_new_game()
        while not self.__sudoku.game_over():
            print(self.__sudoku)
            row, col, num = input("Enter the row, column, and value >").split()
            self.__sudoku.guess_number(Guess(int(row)-1, int(col)-1, int(num)))


    def __print_difficulty_menu(self) -> list[int]:
        print("\n== Select Difficulty ==")
        print("\t1) Easy")
        print("\t2) Medium")
        print("\t3) Hard")
        return [1, 2, 3]


    def __print_welcome_menu(self) -> list[int]:
        print("\t== Menu ==")
        print("\t\t1) Start New Game")
        print("\t\t2) Exit")
        return [1, 2]

    def __get_user_input(self, menu) -> int:
        choices: list[int] = menu()
        while True:
            try:
                option = int(input("\tPlease choose an option >"))
                if option < choices[0] or option > choices[-1]:
                    print("Must choose an available option")
                else:
                    return option
            except ValueError as e:
                print("Must enter a number")


