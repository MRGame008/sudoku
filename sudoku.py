import matplotlib.pyplot as plt
import numpy as np
import copy

class SudokuSolver:
    def __init__(self, grid):
        self.grid = grid
        # Initialize domains for each cell with the full set of values (1 to 9)
        self.domains = [[set(range(1, 10)) if value == 0 else set() for value in row] for row in grid]
    
    def print_domains(self):
        for row in self.domains:
            print(row)

    def is_valid_assignment(self, row, col, num):
        # Check if assigning 'num' to grid[row][col] is valid
        # Check row
        if num in self.grid[row]:
            return False
        # Check column
        if num in [self.grid[i][col] for i in range(9)]:
            return False
        # Check subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.grid[i][j] == num:
                    return False
        return True

    def forward_checking(self, row, col, num):
        # Reduce the domain of adjacent cells based on the assignment
        for i in range(9):
            if i != col and num in self.domains[row][i]:
                self.domains[row][i].remove(num)
            if i != row and num in self.domains[i][col]:
                self.domains[i][col].remove(num)

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if i != row and j != col and num in self.domains[i][j]:
                    self.domains[i][j].remove(num)

    def solve_hard_sudoku(self):
        empty_cell = self.find_empty_cell()
        
        if not empty_cell:
            return True
        
        row, col = empty_cell

        for num in range(1, 10):
            if self.is_valid_assignment(row, col, num):
                self.grid[row][col] = num

                self.forward_checking(row, col, num)

                if self.solve_hard_sudoku():
                    return True

                self.grid[row][col] = 0

        return False


    def solve_sudoku(self):
        empty_cell = self.find_empty_cell()

        if not empty_cell:
            return True

        row, col = empty_cell

        for num in list(self.domains[row][col]):
            if self.is_valid_assignment(row, col, num):
                self.grid[row][col] = num

                # Backup the domains before forward checking
                backup_domains = copy.deepcopy(self.domains)

                self.forward_checking(row, col, num)

                if self.solve_sudoku():
                    return True

                # Restore the domains if the assignment does not lead to a solution
                self.domains = backup_domains
                self.domains[row][col] -= {num}
                self.grid[row][col] = 0

        return False


    def find_empty_cell(self):
        # Find the first empty cell in the grid
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return i, j
        return None

def draw_sudoku(grid):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.matshow(np.ones_like(grid) * -1, cmap="Blues", vmin=-2, vmax=2)

    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                ax.text(j, i, str(grid[i][j]), ha='center', va='center', fontsize=12, fontweight='bold')

    for i in range(1, 9):
        linewidth = 2 if i % 3 == 0 else 0.5
        ax.axhline(i - 0.5, color='black', linewidth=linewidth)
        ax.axvline(i - 0.5, color='black', linewidth=linewidth)

    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()

# Hard Example :
# sudoku_grid = [
#     [0, 0, 0, 0, 0, 0, 0, 4, 0],
#     [3, 0, 0, 0, 0, 1, 7, 2, 0],
#     [0, 5, 0, 0, 0, 0, 8, 0, 0],
#     [0, 0, 0, 0, 0, 2, 0, 0, 0],
#     [0, 0, 0, 5, 6, 0, 0, 0, 0],
#     [6, 0, 3, 0, 0, 7, 2, 0, 4],
#     [1, 3, 0, 0, 8, 0, 0, 7, 0],
#     [5, 9, 0, 0, 3, 0, 1, 0, 2],
#     [0, 0, 4, 2, 0, 9, 0, 0, 8]
# ]

# sudo = SudokuSolver(sudoku_grid)
# foundAnswer = sudo.solve_hard_sudoku()
# print(foundAnswer)
# for row in sudo.grid:
#     print(row)

# Simple Example
sudoku_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

sudo = SudokuSolver(sudoku_grid)
foundAnswer = sudo.solve_sudoku()
print(foundAnswer)
for row in sudo.grid:
    print(row)

draw_sudoku(sudo.grid)

