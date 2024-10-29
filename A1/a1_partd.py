# Finds overflowing cells in a 2D grid and returns them.
# Overflow happens if the absolute value of a cell's content
# is greater or equal of the number of neighbors
def get_overflow_list(grid):
    
    rows = len(grid)
    columns = len(grid[0])
    result = []
    
    for i in range(rows):
        for j in range(columns):
           
            neighbors = 0

            if i == 0 or i == rows - 1:  
                neighbors += 1
            else:
                neighbors += 2
            
            if j == 0 or j == columns - 1:  
                neighbors += 1
            else:
                neighbors += 2
            
            cell_value = absolute_value(grid[i][j])
            
            if cell_value >= neighbors:
                result.append((i, j))
    
    return result if result else None


# Custom absolute value function
# Returns the absolute value of the specified number
def absolute_value(number):
    return number if number >= 0 else -number


# Checks whether all the cells in the grid passed as an argument have the same sign
# Returns True if all the sells have same sign, otherwise returns False
# grid - a grid to be checked
# For base condition of overflow function
def all_same_signs(grid): 
    non_zero_cells = []
    for row in grid:
        for cell in row:
            if cell != 0:
                non_zero_cells.append(cell)
    
    if not non_zero_cells:
        return False
    
    sign_of_first = non_zero_cells[0] > 0
    for cell in non_zero_cells:
        sign_of_sell = cell > 0
        if sign_of_sell != sign_of_first:
            return False
    return True
   

# Returns true if a cell has an overflowing neighbor
# or false if it does not have any
def has_adjacent_overflow(r, c, overflow_list):
    if (r - 1, c) in overflow_list:
        return True
    if (r + 1, c) in overflow_list:
        return True
    if (r, c - 1) in overflow_list:
        return True
    if (r, c + 1) in overflow_list:
        return True
    return False


# Modifies a grid based on overflow_list
def overflow_grid(grid, overflow_list):
    
    rows = len(grid)  
    columns = len(grid[0])
        
    for r, c in overflow_list:

        # Store the original sign of the overflowing cell
        overflowing_cell_sign = 1 if grid[r][c] >= 0 else -1

        # Set the value of the overflowing cell to 1
        # if it has an overflowing neighbor or to 0 if id does not have such neighbors
        if has_adjacent_overflow(r, c, overflow_list):
            grid[r][c] = 1
        else:
            grid[r][c] = 0
        
        # Set the increment sign to the sign of the overflowing cell
        increment = 1 if overflowing_cell_sign > 0 else -1

        # Change the sign of the cells around of the overflowing sell and increment or decrement them
        # Upper cell
        if r > 0 and (r - 1, c) not in overflow_list:  
            grid[r - 1][c] = absolute_value(grid[r - 1][c]) * overflowing_cell_sign + increment
        # Lower cell
        if r < rows - 1 and (r + 1, c) not in overflow_list:  
            grid[r + 1][c] = absolute_value(grid[r + 1][c]) * overflowing_cell_sign + increment
        # Left cell
        if c > 0 and (r, c - 1) not in overflow_list: 
            grid[r][c - 1] = absolute_value(grid[r][c - 1]) * overflowing_cell_sign + increment
        # Right cell
        if c < columns - 1 and (r, c + 1) not in overflow_list:  
            grid[r][c + 1] = absolute_value(grid[r][c + 1]) * overflowing_cell_sign + increment

# Recursively modifies the grid until no more overflow conditions are met
def overflow(grid, a_queue):
    
    overflow_list = get_overflow_list(grid)
    if overflow_list is None or all_same_signs(grid):
        return 0
    overflow_grid(grid, overflow_list) 
    
    # Creates a copy of the grid and enqueues it     
    a_queue.enqueue([row.copy() for row in grid])
    return 1 + overflow(grid, a_queue)
