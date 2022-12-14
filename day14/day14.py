import os
import copy

#-----------------------------------------------------------------------------
def print_cave(cave, x_offset):
    for y in range(0, len(cave[0])):
        for x in range(-1, len(cave)):
            if x < 0:
                print("{:3d}".format(y), end='')
            else:
                if y == 0 and x + x_offset == 500:
                    print('+', end='')
                else:
                    print(cave[x][y], end='')
        print('')
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    file_list = os.listdir()
    for i in range(0, len(file_list)):
        print("{}\t{}".format(i, file_list[i]))

    try:
        fname = file_list[int(input("Line Number: "))]
    except IndexError or ValueError:
        fname = "cave.txt"

    f = open(fname, 'r')

    cave = [['.']] # columns of rows
    x_offset = None
    last_pt = None
    for line in f:
        points = line.split('->')
        last_pt = None
        for point in points:
            x_y = point.strip().split(',')
            if x_offset is None:
                x_offset = int(x_y[0])
                x = 0
            else:
                x = int(x_y[0]) - x_offset

            y = int(x_y[1])
            # print("x,y = {},{}".format(x, y))

            while x < 0:
                # expand cave left
                empty_col = []
                for unit in cave[0]:
                    empty_col.append('.')
                cave.insert(0, empty_col)
                x += 1
                x_offset -= 1
                if last_pt is not None:
                    last_pt[0] += 1

            while x > len(cave) - 1:
                # expand cave RIGHT
                empty_col = []
                for unit in cave[0]:
                    empty_col.append('.')
                cave.append(empty_col)
            
            while y > len(cave[0]) - 1:
                # expand cave down
                for col_ind in range(0, len(cave)):
                    cave[col_ind].append('.')

            # draw rock
            if last_pt is not None:
                if last_pt[0] != x:
                    # draw horizontal rock
                    if last_pt[0] < x:
                        for i in range(last_pt[0], x + 1):
                            cave[i][y] = '#'
                    else:
                        for i in range(x, last_pt[0] + 1):
                            cave[i][y] = '#'

                elif last_pt[1] != y:
                    # draw vertical rock
                    if last_pt[1] < y:
                        for i in range(last_pt[1], y + 1):
                            cave[x][i] = '#'
                    else:
                        for i in range(y, last_pt[1] + 1):
                            cave[x][i] = '#'

            last_pt = [x, y]
            # END FOR POINT IN POINTS

        # print_cave(cave, x_offset)

    f.close()

    cave_og = copy.deepcopy(cave)
    x_offset_og = x_offset

    print("="*79)
    print("    EMPTY CAVE ")
    print_cave(cave, x_offset)
    print("="*79)

    # BEGIN PART 1 SAND SIMULATION
    sand_count = 0

    done = False
    origin = 500 - x_offset
    while not done:
        at_rest = False
        x = origin
        y = 0

        while not at_rest:
            
            # always ensure we have a new column at the left or right 
            # if we're even close to those extremes
            if x <= 0:
                new_col = []
                for unit in cave[0]:
                    new_col.append('.')
                cave.insert(0, new_col)
                x += 1
                x_offset += 1
            elif x >= len(cave) - 1:
                new_col = []
                for unit in cave[0]:
                    new_col.append('.')
                cave.append(new_col)

            try:
                # check if we're blocked from going straight down
                if cave[x][y + 1] != '.':
                    # straight down is blocked, check left diagonal
                    if cave[x-1][y + 1] != '.':
                        # left diagonal is blocked, try right diagonal
                        if cave[x+1][y+1] != '.':
                            # final direction is blocked, place sand at present location
                            at_rest = True
                        else:
                            # right diagonal is OK
                            x += 1
                            y += 1
                    else:
                        # left diagonal is OK
                        x -= 1
                        y += 1
                else:
                    # straight down is OK
                    y += 1
            except IndexError:
                print("Index error")
                done = True
                break

        if at_rest:
            sand_count += 1
            cave[x][y] = 'o'
        # print_cave(cave, x_offset)

    print_cave(cave, x_offset)

    ##### SETUP CAVE #####
    cave_w_floor = copy.deepcopy(cave_og)
    x_offset = x_offset_og

    for i in range(0, len(cave_w_floor)):
        cave_w_floor[i].append('.')
        cave_w_floor[i].append('#')

    print_cave(cave_w_floor, x_offset)
    print("Units of sand at rest: {}".format(sand_count))

    ######## SIMULATE FINAL #########
    sand_count = 0

    done = False
    origin = 500 - x_offset
    while not done:
        at_rest = False

        # starting point
        x = 500 - x_offset 
        y = 0

        if cave_w_floor[x][y] == 'o':
            break

        while not at_rest:
            
            # always ensure we have a new column at the left or right 
            # if we're even close to those extremes
            # INCLUDE FLOOR THIS TIME
            if x <= 0:
                new_col = []
                for i in range(0, len(cave_w_floor[0]) - 1):
                    new_col.append('.')
                new_col.append('#') # create the floor
                cave_w_floor.insert(0, new_col)
                x += 1
                x_offset -= 1
            elif x >= len(cave_w_floor) - 1:
                new_col = []
                for i in range(0, len(cave_w_floor[0]) - 1):
                    new_col.append('.')
                new_col.append('#') # add floor
                cave_w_floor.append(new_col)

            # check if we're blocked from going straight down
            if cave_w_floor[x][y + 1] != '.':
                # straight down is blocked, check left diagonal
                if cave_w_floor[x-1][y + 1] != '.':
                    # left diagonal is blocked, try right diagonal
                    if cave_w_floor[x+1][y+1] != '.':
                        # final direction is blocked, place sand at present location
                        at_rest = True
                    else:
                        # right diagonal is OK
                        x += 1
                        y += 1
                else:
                    # left diagonal is OK
                    x -= 1
                    y += 1
            else:
                # straight down is OK
                y += 1
            

        if at_rest:
            sand_count += 1
            cave_w_floor[x][y] = 'o'
            
        # print_cave(cave_w_floor, x_offset)
        # input("PAUSING (PRESS ENTER)")

    print_cave(cave_w_floor, x_offset)

    print("Considering the floor, {} units of sand fill the cave.".format(sand_count))