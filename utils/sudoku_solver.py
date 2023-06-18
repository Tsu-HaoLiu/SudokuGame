# imports
import random
from copy import *


class SudokuBoard:
    def __init__(self, board: list[list] = None):
        if board is None:
            board = []

        self.board = board
        self.board_size = len(self.board)
        self.valid_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.difficulty = {
            'beginner': 24,
            'easy': 37,
            'medium': 47,
            'hard': random.randint(49, 53),
            'extreme': random.randint(54, 59),
        }

    def generate(self):
        """Generate a solved sudoku board"""
        self.set_empty_board()
        randomize_first_row = self.valid_numbers.copy()
        random.shuffle(randomize_first_row)  # randomize a list 1-9
        self.board[0] = randomize_first_row  # set first row as randomized list
        self.board_length()
        self.solve()
        return self.board

    def scrambled_board(self, difficulty_setting: str = 'beginner') -> list[list]:
        """A function to remove numbers from the fully solved sudoku board depending on difficulty

        :param difficulty_setting: Takes difficulty inputs `beginner` (default), `easy`, `medium`, `hard`, `extreme`
        :return: Unsolved sudoku board
        """

        sudoku_copy = deepcopy(self.board)
        difficulty_setting = difficulty_setting.lower()
        removals = self.difficulty.get(difficulty_setting, 24)

        i = 0
        while i < removals:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if sudoku_copy[row][col] != 0:
                sudoku_copy[row][col] = 0
                i += 1

        return sudoku_copy

    def board_length(self):
        self.board_size = len(self.board)

    def set_empty_board(self):
        self.board = [[0] * 9 for _ in range(9)]

    def set_board(self, board):
        self.board = board
        print(*self.board, sep='\n')
        self.board_size = len(self.board) if self.board else 0

    def is_solvable(self):
        return bool(self.solve())

    def is_valid(self, row, col, num):
        """Validate the num in the board is valid on both row, col and 3x3 box"""

        # Check if the number is already present in the column
        for i in range(9):
            if self.board[i][col] == num:
                return False

        # Check if the number is already present in the 3x3 grid
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False

        # If the number is valid, return True
        return num not in self.board[row]

    def solve(self):
        """Solve the sudoku board using recursion"""
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == 0:
                    for n in range(1, 10):
                        if self.is_valid(row, col, n):
                            self.board[row][col] = n
                            if self.solve():
                                return self.board
                            self.board[row][col] = 0
                    return False
        return True


