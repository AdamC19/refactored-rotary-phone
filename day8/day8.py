import os

DIR_NORTH = 0
DIR_EAST = 1
DIR_SOUTH = 2
DIR_WEST = 3


#------------------------------------------------------------------------------
def get_scenic_score(location, forest):
    """location is a tuple (row, col). forest is a list of lists of ints."""
    try:
        current_col = location[1]
        current_row = location[0]
        n_cols = len(forest[0])
        n_rows = len(forest)
        this_height = forest[current_row][current_col]
    except IndexError:
        return 0, []

    north_count = 1
    east_count = 1
    south_count = 1
    west_count = 1

    # NORTH look at all lower indexed rows at current column
    if(current_row > 0):
        while current_row - north_count > 0 and forest[current_row - north_count][current_col] < this_height:
            north_count += 1
    else:
        return 0, []

    # EAST look at all higher indexed columns at current row
    if current_col < n_cols - 1:
        while current_col + east_count < n_cols - 1 and forest[current_row][current_col + east_count] < this_height:
            east_count += 1
    else:
        return 0, []

    # SOUTH look at all higher indexed rows at current column
    if current_row < n_rows - 1:
        while current_row + south_count < n_rows - 1 and forest[current_row + south_count][current_col] < this_height:
            south_count += 1
    else:
        return 0, []

    # WEST look at all lower indexed columns at current row
    if current_col > 0:
        while current_col - west_count > 0 and forest[current_row][current_col - west_count] < this_height:
            west_count += 1
    else:
        return 0, []

    return north_count * east_count * south_count * west_count, [north_count, east_count, south_count, west_count]

#------------------------------------------------------------------------------
def get_max_height_in_direction(direc: int, location, forest) -> int:
    """location is a tuple (row, col). forest is a list of lists of ints."""
    
    try:
        current_col = location[1]
        current_row = location[0]
        n_cols = len(forest[0])
        n_rows = len(forest)
    except IndexError:
        return -1

    max_height = 0

    if direc == DIR_NORTH:
        # look at all lower indexed rows at current column
        for row in range(current_row - 1, -1, -1): # stop is -1 because we need to look at the exterior-most tree
            if forest[row][current_col] == 9:
                max_height = 9
                break # no need to proceed, since we found the maximum allowed value
            elif forest[row][current_col] > max_height:
                max_height = forest[row][current_col]

    elif direc == DIR_EAST: 
        # look at all higher indexed columns at current row
        for col in range(current_col + 1, n_cols, 1):
            if forest[current_row][col] == 9:
                max_height = 9
                break
            elif forest[current_row][col] > max_height:
                max_height = forest[current_row][col]

    elif direc == DIR_SOUTH:
        # look at higher indexed rows at current column
        for row in range(current_row + 1, n_rows, 1): # 
            if forest[row][current_col] == 9:
                max_height = 9
                break # no need to proceed, since we found the maximum allowed value
            elif forest[row][current_col] > max_height:
                max_height = forest[row][current_col]

    elif direc == DIR_WEST:
        # look at lower indexed columns at current row
        for col in range(current_col - 1, -1, -1):
            if forest[current_row][col] == 9:
                max_height = 9
                break
            elif forest[current_row][col] > max_height:
                max_height = forest[current_row][col]

    else:
        return -1 # not a valid direction

    return max_height
#------------------------------------------------------------------------------


file_list = os.listdir()
for i in range(0, len(file_list)):
    print("{}\t{}".format(i, file_list[i]))

try:
    fname = file_list[int(input("Line Number: "))]
except IndexError or ValueError:
    fname = "trees.txt"

f_trees = open(fname, 'r')


forest = []

for row in f_trees:
    row_arr = []
    for c in row.strip():
        row_arr.append(int(c))

    forest.append(row_arr)


row_count = len(forest)
col_count = len(forest[0])
n_trees = row_count * col_count
print("We have {} rows and {} columns of trees, for a forest of {} trees.".format(row_count, col_count, n_trees))

# initialize with number of trees around the edges
n_visible_trees = 2*col_count + 2*(row_count - 2)

for row_ind in range(1, row_count - 1):
    for col_ind in range(1, col_count - 1):
        height = forest[row_ind][col_ind]
        invisible = True
        for direc in range(0, 4):
            max_h = get_max_height_in_direction(direc, (row_ind, col_ind), forest)
            invisible = invisible and height <= max_h
            if not invisible:
                break
        if not invisible:
            n_visible_trees += 1

print("Looks like we have {} visible trees, and {} trees suitable for a treehouse.".format(n_visible_trees, n_trees - n_visible_trees))

max_scenic_score = 1
max_comp = []
for row_ind in range(1, row_count - 1):
    for col_ind in range(1, col_count - 1):
        score, comp = get_scenic_score((row_ind, col_ind), forest)
        if score > max_scenic_score:
            max_scenic_score = score
            max_comp = comp

print("The highest scenic score in our forest is {}.".format(max_scenic_score))
print("Comprised of : ", end='')
print(max_comp)