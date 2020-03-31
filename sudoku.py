from functools import reduce

def solve(grid):
    """Backtracking algorithm that solves a sudoku puzzle"""

    # Get all cells that need to be filled in
    variables = getVariables(grid)

    def solver(grid, variables):
        """Recursive function that solves the sudoku puzzle"""

        # Base case: if no more empty cells, then finish
        if not variables:
            return True

        i, j = variables[0] # Get position of the cell in the puzzle

        # Iterate through all the possible values
        for value in range(1,10):

            # Check if it is a valid input
            if valid(grid, value, (i, j)):
                grid[i][j] = value

                # Check if this valid input works for future inputs
                if solver(grid, variables[1:]):
                    return True

                # Reset because it doesn't produce a valid solution
                grid[i][j] = 0

        return False

    return solver(grid, variables)


def valid(grid, value, pos):
    """Checks whether the given value is a valid input"""
    
    # Check row
    if value in set(grid[pos[0]]):
        return False

    # Check column
    if value in set([grid[i][pos[1]] for i in range(len(grid[0]))]):
        return False

    # Check box
    if value in set([grid[i][j] for i in range((pos[0]//3) * 3, (pos[0]//3) * 3 + 3) for j in range((pos[1]//3) * 3, (pos[1]//3) * 3 + 3)]):
        return False

    return True


def printGrid(grid):
    """Artfully prints a sudoku grid"""

    # Iterate each row
    for i in range(len(grid)):
        row = grid[i][:]       # Copy row

        for x in [9, 6, 3, 0]:
            row.insert(x, "|") # Insert column dividers

        if i % 3 == 0:
            print("-"*13)      # Print row dividers

        # Reduce the row down to one string and print
        print(reduce(lambda x, y: x + y, map(lambda x: str(x), row)))

    # Finish the last row divider
    print("-"*13)


def getVariables(grid):
    """Gets all the empty cells from the grid"""
    return [(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == 0]

################
"""
530070000
600195000
098000060
800060003
400803001
700020006
060000280
000419005
000080079
"""

def makeGrid():
    """Take in a user input row by row to create grid.
    Use 0 to represent an empty cell
    """
    return [list(map(int, input())) for i in range(9)]

def test():
    """Test the functionality of it by hand because doctests would be way to long"""
    grid = makeGrid()
    solve(grid)
    printGrid(grid)















