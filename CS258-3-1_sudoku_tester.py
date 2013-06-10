__author__ = 'Russ'

# SPECIFICATION:
#
# check_sudoku() determines whether its argument is a valid Sudoku
# grid. It can handle grids that are completely filled in, and also
# grids that hold some empty cells where the player has not yet
# written numbers.
#
#
# If the sanity checks pass, your code should return True if all of
# the following hold, and False otherwise:
#
#
# This diagram (which depicts a valid Sudoku grid) illustrates how the
# grid is divided into sub-grids:
#
# 5 3 4 | 6 7 8 | 9 1 2
# 6 7 2 | 1 9 5 | 3 4 8
# 1 9 8 | 3 4 2 | 5 6 7
# ---------------------
# 8 5 9 | 7 6 1 | 4 2 3
# 4 2 6 | 8 5 3 | 7 9 1
# 7 1 3 | 9 2 4 | 8 5 6
# ---------------------
# 9 6 1 | 5 3 7 | 0 0 0
# 2 8 7 | 4 1 9 | 0 0 0
# 3 4 5 | 2 8 6 | 0 0 0
#
# Please keep in mind that a valid grid (i.e., one for which your
# function returns True) may contain 0 multiple times in a row,
# column, or sub-grid. Here we are using 0 to represent an element of
# the Sudoku grid that the player has not yet filled in.

# check_sudoku should return None
ill_formed = [[5,3,4,6,7,8,9,1,2],
              [6,7,2,1,9,5,3,4,8],
              [1,9,8,3,4,2,5,6,7],
              [8,5,9,7,6,1,4,2,3],
              [4,2,6,8,5,3,7,9],  # <---
              [7,1,3,9,2,4,8,5,6],
              [9,6,1,5,3,7,2,8,4],
              [2,8,7,4,1,9,6,3,5],
              [3,4,5,2,8,6,1,7,9]]

ill_formed2 = [[5,3,4,6,7,8,9,1,2],
               [6,7,2,1,9,5,3,4,8],
               [1,9,8,3,4,'x',5,6,7],
               [8,5,9,7,6,1,4,2,3],
               [4,2,6,10,5,3,7,9,1],
               [7,1,3,9,2,4,8,5,6],
               [9,6,1,5,3,7,2,8,4],
               [2,8,7,4,1,9,6,3,5],
               [3,4,5,2,8,6,1,7,9]]

# check_sudoku should return True
valid = [[5,3,4,6,7,8,9,1,2],
         [6,7,2,1,9,5,3,4,8],
         [1,9,8,3,4,2,5,6,7],
         [8,5,9,7,6,1,4,2,3],
         [4,2,6,8,5,3,7,9,1],
         [7,1,3,9,2,4,8,5,6],
         [9,6,1,5,3,7,2,8,4],
         [2,8,7,4,1,9,6,3,5],
         [3,4,5,2,8,6,1,7,9]]

# check_sudoku should return False
invalid = [[5,3,4,6,7,8,9,1,2],
           [6,7,2,1,9,5,3,4,8],
           [1,9,8,3,8,2,5,6,7],
           [8,5,9,7,6,1,4,2,3],
           [4,2,6,8,5,3,7,9,1],
           [7,1,3,9,2,4,8,5,6],
           [9,6,1,5,3,7,2,8,4],
           [2,8,7,4,1,9,6,3,5],
           [3,4,5,2,8,6,1,7,9]]

# check_sudoku should return True
easy = [[2,9,0,0,0,0,0,7,0],
        [3,0,6,0,0,8,4,0,0],
        [8,0,0,0,4,0,0,0,2],
        [0,2,0,0,3,1,0,0,7],
        [0,0,0,0,8,0,0,0,0],
        [1,0,0,9,5,0,0,6,0],
        [7,0,0,0,9,0,0,0,1],
        [0,0,1,2,0,0,3,0,6],
        [0,3,0,0,0,0,0,5,9]]

# check_sudoku should return True
hard = [[1,0,0,0,0,7,0,9,0],
        [0,3,0,0,2,0,0,0,8],
        [0,0,9,6,0,0,5,0,0],
        [0,0,5,3,0,0,9,0,0],
        [0,1,0,0,8,0,0,0,2],
        [6,0,0,0,0,4,0,0,0],
        [3,0,0,0,0,0,0,1,0],
        [0,4,0,0,0,0,0,0,7],
        [0,0,7,0,0,0,3,0,0]]

def columns(grid):
    """
    Returns columns from a grid.
    """
    return [[r[col] for r in grid] for col in range(len(grid))]


def subgrids(grid, d=3):
    """
    Returns the 3x3 subgrids from a 9x9 grid.
    """
    return [[i for row in grid[y:y+d] for i in row[x:x+d]]
            for x in range(0, len(grid), d)
            for y in range(0, len(grid), d)]

def check_sudoku(grid):
    valid_chars = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # 9x9 list of lists
    if len(grid) != 9 or not all(map(lambda x: x == 9, [len(r) for r in grid])):
        return None

    # contains, in each of its 81 elements, an integer in the range 0..9
    if not all([i in valid_chars for r in grid for i in r]):
        return None

    # each number in the range 1..9 occurs only once in each row
    if any(r.count(i) > 1 for r in grid for i in range(1, 10)):
        return False

    # each number in the range 1..9 occurs only once in each column
    if any(c.count(i) > 1 for c in columns(grid) for i in range(1, 10)):
        return False

    # each number the range 1..9 occurs only once in each of the nine
    # 3x3 sub-grids, or "boxes", that make up the board
    if any(g.count(i) > 1 for g in subgrids(grid) for i in range(1, 10)):
        return False

    return True

assert columns(hard)[0] == [1, 0, 0, 0, 0, 6, 3, 0, 0]
assert subgrids(hard)[0] == [1, 0, 0, 0, 3, 0, 0, 0, 9]
assert check_sudoku(ill_formed) is None
assert check_sudoku(ill_formed2) is None
assert check_sudoku(valid) is True
assert check_sudoku(invalid) is False
assert check_sudoku(easy) is True
assert check_sudoku(hard) is True


