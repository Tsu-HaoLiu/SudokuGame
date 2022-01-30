import random
import time
from copy import *


class BackwardIterator:
    def __init__(self, iterator):
        self.iterator = iterator
        self.history = [None, ]
        self.i = 0

    def next(self):
        self.i += 1
        if self.i < len(self.history):
            return self.history[self.i]
        else:
            elem = next(self.iterator)
            self.history.append(elem)
            return elem

    def prev(self):
        self.i -= 1
        if self.i == 0:
            raise StopIteration
        else:
            return self.history[self.i]


class SudokuCore:

    def __init__(self, board: list[list] = None, method: str = None):
        """Initializing variables

        :param board: *Optional* adding a `board` on init instead of calling `addboard` function
        :param method: *Optional* adding a `method` on init instead of calling `setmethod` function
        """
        self.saved_position = {}
        self.boardlength = 0
        self.ogcopy = []
        self.board_col = []
        self.three_by = []
        self.unsolved_board = []
        self.ee = 3  # magic number to calculate 3x3 sudoku blocks
        self.fixed_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.emptyboard = [[0] * 9 for _ in range(9)]
        self.board = self.addboard(board) if isinstance(board, list) else None
        self.method = self.setmethod(method) if isinstance(method, str) else "recursion"
        self.on_init()

    def on_init(self):
        """Directly solve board if board and method are given on init"""
        if isinstance(self.board, list) and isinstance(self.method, str):
            return self.solve()

    def addboard(self, board: list[list]):
        """A function to make a deep copy of the board and create alternative boards."""

        self.board = deepcopy(board)
        self.ogcopy = deepcopy(board)
        self.boardlength = len(self.board)
        self.fix_table()
        return self.board

    def setmethod(self, method: str):
        """A function to set a method for solving a sudoku.
        If no method is set, method `recursion` will be defaulted.

        :param method: A str containing `recursion`, `sorted_recursion`, `generate`
        :return: Nothing
        """
        self.method = method
        return self.method

    def fix_table(self):
        """ A function to reevaluate the column and 3 by 3 board."""
        self.board_col = list(map(list, zip(*self.board)))
        self.three_by = [[self.board[(j // self.ee) * self.ee + i // self.ee][(j % self.ee) * self.ee + i % self.ee]
                          for i in range(self.boardlength)] for j in range(self.boardlength)]
        return

    def possible_numbers(self, row, col, n, method=None):
        """This function is to check unused numbers (1-9) in row/column/3x3.

        :param row: An integer representing the rows on the board
        :param col: An integer representing the columns on the board
        :param n: The number that is evaluated
        :param method: A method in which to return the information
        :return: Depending on the method this function can return a `Boolean` or `List`
        """
        self.fix_table()
        possible = list(set(self.fixed_list) - set(self.board[row]) - set(self.board_col[col]) - set(self.three_by[(row//self.ee)*self.ee+col//self.ee]))
        possible.sort()

        if method == "recursion":
            return True if n in possible else False
        elif method == "scan":
            return possible
        elif method == "sorted_recursion":
            if n in possible:
                return True
            elif len(possible) == 1 and possible[0] == 0:
                return 0
        return False

    def recursion(self):
        """A function to solve a sudoku board by recursion and backtracking. (Depth-first search)
        Loops through row -> column checks square is 0 then try numbers from 1-9
        If possible_numbers (1-9) check is `False` set square back to 0 and try the next number

        :return: Nothing
        """

        if self.method == "generate" and not self.board:
            self.addboard(self.emptyboard)
            randomize_first_row = self.fixed_list.copy()
            random.shuffle(randomize_first_row)  # randomize a list 1-9

        for row in range(self.boardlength):
            for col in range(self.boardlength):
                if self.board[row][col] == 0:
                    if row == 0 and self.method == "generate":  # insert first row to make board random
                        self.board[row] = randomize_first_row
                        continue
                    for n in range(1, 10):
                        if self.possible_numbers(row, col, n, method="recursion"):
                            self.board[row][col] = n
                            if self.recursion():
                                return self.board
                            self.board[row][col] = 0
                    return False
        return True

    def generate(self, dif: str = "beginner") -> list[list]:
        """This function calls other functions to generate and return an unfinished sudoku board.

        :param dif: Takes difficulty inputs `beginner` (default), `easy`, `medium`, `hard`, `extreme`
        :return: An unsolved sudoku board
        """
        self.method = "generate"
        return self.remove_num(self.recursion(), dif)

    def solved_board(self):
        return self.board

    def remove_num(self, board: list[list], dif: str) -> list[list]:
        """A function to remove numbers from the fully solved sudoku board depending on difficulty

        :param board: Fully solved sudoku board
        :param dif: Takes difficulty inputs `beginner` (default), `easy`, `medium`, `hard`, `extreme`
        :return: Unsolved sudoku board
        """
        i = 0
        solved_board = deepcopy(board)
        dif = dif.lower()
        removals = 24  # beginner

        if dif == 'easy':
            removals = 37
        elif dif == 'medium':
            removals = 47
        elif dif == 'hard':
            removals = random.randint(49, 53)
        elif dif == 'extreme':
            removals = random.randint(54, 59)

        while i < removals:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if solved_board[row][col] != 0:
                solved_board[row][col] = 0
                i += 1

        self.unsolved_board = deepcopy(solved_board)
        return solved_board

    def sorted_recursion_action(self, sort_iter_keys, sort_saved_pos, iter_pos):
        row, col = int(iter_pos[0]), int(iter_pos[-1])
        for n in sort_saved_pos[iter_pos]:
            if self.possible_numbers(row, col, n, method="recursion"):
                self.board[row][col] = n
                iter_pos = sort_iter_keys.next()
                self.sorted_recursion_action(sort_iter_keys, sort_saved_pos, iter_pos)
                iter_pos = sort_iter_keys.prev()
                self.board[row][col] = 0
        return

    def sorted_recursion(self):
        """A function to solve a sudoku board with pre-scanned numbers and positions.
        This method will save more time, compared to standard recursion,
        by only processing specific positions and possible numbers.

        :return: Boolean: `True` if board is solved and `False` if board remains unsolved.
        """
        sort_saved_pos = self.saved_position
        sort_iter_keys = BackwardIterator(iter(sort_saved_pos))
        iter_pos = sort_iter_keys.next()
        try:
            self.sorted_recursion_action(sort_iter_keys, sort_saved_pos, iter_pos)
        except StopIteration:
            if all(col != 0 and row != 0 for row in self.board for col in row):
                return True  # check to see if board is zeroless
            return False

    def possible_positions(self):
        """This function scans the row -> column and finds all possible numbers that
        can fit in the empty square and save it in a list.

        [3, 8, [9, 2, 1], 7, 5, [4, 9, 2, 1], [2, 3, 6]]
        :return: Boolean `True` or `False` if board was solvable.
        """
        m = 0
        while m < 2:
            m += 1
            splength = len(self.saved_position)
            for row in range(self.boardlength):
                for col in range(self.boardlength):
                    if self.board[row][col] != 0:
                        continue
                    # returns list of possible numbers
                    possible = self.possible_numbers(row, col, 0, method="scan")

                    # If there is only one number in the list just replace empty cell with number
                    if len(possible) == 1:
                        self.ogcopy[row][col] = possible[0]
                        self.board[row][col] = possible[0]
                        if self.saved_position.get(str(row) + str(col)):
                            del self.saved_position[str(row) + str(col)]
                    else:
                        self.saved_position[str(row) + str(col)] = possible
                        self.ogcopy[row][col] = possible

            # if the length of saved_position changes (meaning a number was inserted into board)
            # try another loop to see if more numbers can be solved.
            if len(self.saved_position) != splength:
                m = 0

        self.fix_table()
        if self.sorted_recursion():
            return True
        else:
            return False

    def solve(self) -> list[list]:
        """Main solve function

        :return: Returns a solved sudoku board
        """
        if self.method is None or self.board is None:
            raise ValueError("Board not initialized: addboard(list[list])")

        if self.method == "recursion":
            solvable = self.recursion()
        else:
            solvable = self.possible_positions()

        # print("board:", *self.board, sep="\n")

        if not solvable:
            raise Exception(f"This board can't be solved with [{self.method}] method")

        return self.board


test_board = [
    [0, 3, 0, 0, 8, 0, 0, 0, 6],
    [2, 0, 0, 0, 0, 0, 7, 0, 3],
    [0, 7, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 1, 2, 0, 0, 0, 0, 0],
    [0, 5, 2, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 6, 7, 0, 0, 0],

    [9, 0, 4, 0, 0, 0, 0, 5, 0],
    [0, 0, 0, 0, 9, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 6, 0, 8, 0]
]

# methods = ["sorted_recursion", "recursion"]
# # meth = "sorted_recursion"
# sds = []
# q = 0
# # while q < 10:
# for meth in methods:
#     q += 1
#     print(f"Running with method [{meth}]")
#     t = time.time()
#     sc = SudokuCore(test_board, meth)
#     # print(sc.board)
#     # sc.addboard(test_board)
#     # sc.setmethod(meth)
#     # sc.solve()
#     ct = time.time() - t
#     sds.append(ct)
#     print(f"Finished: {ct:.4f}s")
#     # time.sleep(2)
# print(sum(sds)/10)
