import numpy as np
from copy import deepcopy
import re

EMPTY = 0


def load_sudokus(file_name):
    sudokus = []
    with open(file_name, "r") as file:
        raw_text = file.read()
        string_pattern = "Grid\\s[0-9]+\n"
        regex_pattern = re.compile(string_pattern)
        sudokus_strings = list(filter(None, re.split(regex_pattern, raw_text)))
        for string in sudokus_strings:
            flatten_sudoku = [int(char) for char in string.replace("\n", "")]
            sudoku = np.array(flatten_sudoku).reshape(9, 9)
            sudokus.append(sudoku)
        return sudokus


def check_rows(matrix):
    for row in matrix:
        row = list(filter(lambda val: val != EMPTY, row))
        if len(row) != len(set(row)):
            return False
    return True


def check_columns(matrix):
    for column in matrix.transpose():
        column = list(filter(lambda val: val != EMPTY, column))
        if len(column) != len(set(column)):
            return False
    return True


def check_squares(matrix):
    for x in range(0, 7, 3):
        for y in range(0, 7, 3):
            square = matrix[np.ix_(list(range(x, x + 3)), list(range(y, y + 3)))]
            square = list(filter(lambda val: val != EMPTY, square.flatten()))
            if len(square) != len(set(square)):
                return False
    return True


def check_board(matrix):
    return check_rows(matrix) and check_columns(matrix) and check_squares(matrix)


def find_next_empty(matrix):
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == EMPTY:
                return i, j
    return None


def solve_sudoku(matrix):
    next_square = find_next_empty(matrix)
    if next_square is None:
        return True
    else:
        row, col = next_square

    for guessed_number in range(1, 10):
        temp_board = deepcopy(matrix)
        temp_board[row][col] = guessed_number
        if check_board(temp_board):
            matrix[row][col] = guessed_number
            if solve_sudoku(matrix):
                return True
            matrix[row][col] = 0

    return False


if __name__ == "__main__":
    sudokus = load_sudokus("sudokus.txt")
    for index, sudoku in enumerate(sudokus):
        print(f"Sudoku #{index +1}:\n {sudoku} \n")
        solve_sudoku(sudoku)
        print(f"Solved sudoku:\n {sudoku} \n")
        print("-----------------------------\n")
