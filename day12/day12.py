import os
import math
import copy
import sys

DIR_LUT = ['^', '>', 'v', '<']

sys.setrecursionlimit(32000)
results = []
#------------------------------------------------------------------------------
class RouteNode(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.north = None
        self.east = None
        self.south = None
        self.west = None
        self.is_end = False
        self.steps = -1
        self.history = []
#------------------------------------------------------------------------------
def get_xy_score(pos, dest, test_dir):
    """ Higher score means one step in the test direction is closer to target """
    delta_y = float(dest[0] - pos[0])
    delta_x = float(dest[1] - pos[1])

    start_dist = math.sqrt(delta_x**2 + delta_y**2)

    if test_dir == 'N':
        delta_y = dest[0] - (pos[0] - 1)
    elif test_dir == 'E':
        delta_x = dest[1] - (pos[1] + 1)
    elif test_dir == 'S':
        delta_y = dest[0] - (pos[0] + 1)
    elif test_dir == 'W':
        delta_x = dest[1] - (pos[1] - 1)

    new_dist = math.sqrt(delta_x**2 + delta_y**2)
    # print("XY score for {} move at {},{} is {}".format(test_dir, pos[0],pos[1], start_dist - new_dist))
    return start_dist - new_dist
#------------------------------------------------------------------------------
def get_h_score(this_height, next_height):
    raw_score = next_height - this_height + 1
#------------------------------------------------------------------------------
def max_plus_index(nums):
    """ returns index, max_value """
    maximum = nums[0]
    greatest_ind = 0
    for i in range(greatest_ind + 1, len(nums)):
        if nums[i] > maximum:
            maximum = nums[i]
            greatest_ind = i
    return greatest_ind, maximum
#------------------------------------------------------------------------------
def build_tree(topo, route: RouteNode, dest, from_dir, step_count):
    pos = [route.row, route.col]
    # if step_count % 100 == 0:
        # print("Step count {}".format(step_count))
    if pos == dest:
        route.is_end = True
        route.steps = step_count
        results.append(route.steps)
        print("Found the end at {} steps!".format(route.steps))
        # print_history(route.history)
        return

    scores = get_scores(topo, pos, dest, from_dir, route.history) # get scores for this position
    if scores == [float('-inf'), float('-inf'), float('-inf'), float('-inf')]:
        print("We've hit a dead end at {} steps.".format(step_count))
        return

    
    for ind in range(0, len(scores)):
        i, score = max_plus_index(scores)
        if scores[i] != float('-inf') and scores[i] >= -1.0:
            # this direction of movement is legal
            if i == 0:
                # NORTH
                route.history[pos[0]][pos[1]] = '^'
                if route.history[pos[0] - 1][pos[1]] == '.':
                    route.north = RouteNode(pos[0] - 1, pos[1])
                    route.north.history = copy.deepcopy(route.history)
                    build_tree(topo, route.north, dest, 'S', step_count + 1)
            elif i == 1:
                # EAST
                route.history[pos[0]][pos[1]] = '>'
                if route.history[pos[0]][pos[1] + 1] == '.':
                    route.east = RouteNode(pos[0], pos[1] + 1)
                    route.east.history = copy.deepcopy(route.history)
                    build_tree(topo, route.east, dest, 'W', step_count + 1)
            elif i == 2:
                # SOUTH
                route.history[pos[0]][pos[1]] = 'v'
                if route.history[pos[0] + 1][pos[1]] == '.':
                    route.south = RouteNode(pos[0] + 1, pos[1])
                    route.south.history = copy.deepcopy(route.history)
                    build_tree(topo, route.south, dest, 'N', step_count + 1)
            elif i == 3:
                # WEST
                route.history[pos[0]][pos[1]] = '<'
                if route.history[pos[0]][pos[1] - 1] == '.':
                    route.west = RouteNode(pos[0], pos[1] - 1)
                    route.west.history = copy.deepcopy(route.history)
                    build_tree(topo, route.west, dest, 'E', step_count + 1)
        scores[i] = float('-inf')
#------------------------------------------------------------------------------
def get_scores(topo, coords, dest_coord, from_direc, hist):
    north_score = float('-inf')
    east_score = float('-inf')
    south_score = float('-inf')
    west_score = float('-inf')
    
    # h_score:
    #   1.5 if we can make upward progress
    #   0.5 for neutral (level) progress
    #   -0.5 for downard progress
    #   -inf if height jump is too great
    # xy_score:
    #   improvement in distance to destination
    # test north (negative rows)
    if coords[0] > 0:
        if from_direc != 'N' and hist[coords[0] - 1][coords[1]] == '.':
            north_h_score = topo[coords[0] - 1][coords[1]] - topo[coords[0]][coords[1]] + 0.5
            if north_h_score > 2:
                north_h_score = float('-inf')
            
            north_xy_score = get_xy_score(coords, dest_coord, 'N')
            north_score = north_h_score * north_xy_score

    # test EAST (positive X)
    if coords[1] < len(topo[0]) - 1:
        if from_direc != 'E' and hist[coords[0]][coords[1] + 1] == '.':
            east_h_score = topo[coords[0]][coords[1] + 1] - topo[coords[0]][coords[1]] + 0.5
            if east_h_score <= 2:
                east_xy_score = get_xy_score(coords, dest_coord, 'E')
                east_score = east_h_score * east_xy_score

    # test SOUTH (positive Y)
    if coords[0] < len(topo) - 1:
        if from_direc != 'S' and hist[coords[0] + 1][coords[1]] == '.':
            south_h_score = topo[coords[0] + 1][coords[1]] - topo[coords[0]][coords[1]] + 0.5
            if south_h_score <= 2:
                south_xy_score = get_xy_score(coords, dest_coord, 'S')
                south_score = south_h_score * south_xy_score

    # test WEST (negative x)
    if coords[1] > 0:
        if from_direc != 'W' and hist[coords[0]][coords[1] - 1] == '.':
            west_h_score = topo[coords[0]][coords[1] - 1] - topo[coords[0]][coords[1]] + 0.5
            if west_h_score <= 2:
                # west_h_score = float('-inf')
                west_xy_score = get_xy_score(coords, dest_coord, 'W')
                west_score = west_h_score * west_xy_score

    return [north_score, east_score, south_score, west_score]
#------------------------------------------------------------------------------
def traverse_tree(route: RouteNode):
    if route.is_end:
        print("Found a path with {} steps.".format(route.steps))
        print_history(route.history)
        # results.append(route.steps)
    else:
        if type(route.north) != type(None):
            traverse_tree(route.north)
        if type(route.east) != type(None):
            traverse_tree(route.east)
        if type(route.south) != type(None):
            traverse_tree(route.south)
        if type(route.west) != type(None):
            traverse_tree(route.west)
    
    # if type(route.north) == type(None) and type(route.east) == type(None) and type(route.south) == type(None) and type(route.west) == type(None):
    #     return -1
    # else:
    
#------------------------------------------------------------------------------
def print_history(history):
    print("="*79)
    for row in history:
        for col in row:
            print(col, end='')
        print('')
    print("="*79)
#------------------------------------------------------------------------------

if __name__ == "__main__":
    file_list = os.listdir()
    for i in range(0, len(file_list)):
        print("{}\t{}".format(i, file_list[i]))

    try:
        fname = file_list[int(input("Line Number: "))]
    except IndexError or ValueError:
        fname = "rope.txt"

    f = open(fname, 'r')

    topo = []
    history_blank = []
    topo_row = 0
    topo_col = 0
    start_coord = [0, 0] # y, x
    dest_coord = [0, 0]   # y, x
    for line in f:
        new_row = []
        hist_row = []
        topo_col = 0
        for c in line.strip():
            if c == 'S':
                start_coord[0] = topo_row
                start_coord[1] = topo_col
                new_row.append(0)
                hist_row.append('S')
            elif c == 'E':
                dest_coord[0] = topo_row
                dest_coord[1] = topo_col
                new_row.append(ord('z') - 97)
                hist_row.append('.')
            else:
                new_row.append(ord(c) - 97)
                hist_row.append('.')
            topo_col += 1
        topo.append(new_row)
        history_blank.append(hist_row)
        topo_row += 1

    print("Start postition is: row={}, col={}".format(start_coord[0], start_coord[1]))
    print("End postition is  : row={}, col={}".format(dest_coord[0], dest_coord[1]))
    
    for row in topo:
        for spot in row:
            print("{:3d}".format(spot), end='')
        print('')
    # for row in history_blank:
    #     for spot in row:
    #         print("{}".format(spot), end='')
    #     print('')

    # CONSTRUCT ROUTES
    at_end = False
    coords = start_coord
    routes = RouteNode(coords[0], coords[1])
    routes.history = copy.deepcopy(history_blank)
    route_start = routes
    steps = 0
    history = copy.deepcopy(history_blank)
    # while not at_end:
    #     try:
    #         # print("Current coordinates: row={}, col={}".format(coords[0], coords[1]))
    #         if coords[0] == dest_coord[0] and coords[1] == dest_coord[1]:
    #             at_end = True
    #         else:
    #             scores = get_scores(topo, coords)

    #             # build out our tree
    #             for i in range(0, len(scores)):
    #                 if scores[i] != float('-inf'):
    #                     if i == 0:
    #                         # NORTH
    #                         routes.north = RouteNode(coords[0] - 1, coords[1])
    #                     elif i == 1:
    #                         # EAST
    #                         routes.east = RouteNode(coords[0], coords[1] + 1)
    #                     elif i == 2:
    #                         # SOUTH
    #                         routes.north = RouteNode(coords[0] + 1, coords[1])
    #                     elif i == 3:
    #                         # WEST
    #                         routes.east = RouteNode(coords[0], coords[1] - 1)

    #                 # else not a legal route

    #             ind, max_score = max_plus_index(scores)

    #             if max_score == float('-inf'):
    #                 # WE'RE STUCK, END ROUTE
    #                 print("We've become stuck somehow.....")
    #                 break
    #             else:
    #                 # print("index of maximum score is {} -> {}".format(ind, max_score))
    #                 if ind == 0:
    #                     # we're heading to the yukon
    #                     history[coords[0]][coords[1]] = '^'
    #                     coords[0] = coords[0] - 1
    #                 elif ind == 1:
    #                     # heading east
    #                     history[coords[0]][coords[1]] = '>'
    #                     coords[1] = coords[1] + 1
    #                 elif ind == 2:
    #                     # heading south
    #                     history[coords[0]][coords[1]] = 'v'
    #                     coords[0] = coords[0] + 1
    #                 elif ind == 3:
    #                     # go west young man
    #                     history[coords[0]][coords[1]] = '<'
    #                     coords[1] = coords[1] - 1
    #                 steps += 1
    #     except KeyboardInterrupt:
    #         at_end = True
    try:
        build_tree(topo, routes, dest_coord, '', 0)
        print("=== TREE BUILDING SUCCESS ===")
    except RecursionError:
        print("*** RECURSION ERROR ***")

    # results = []
    # traverse_tree(route_start)
    min_steps = min(results)

    # print("="*79)
    # print(" "*36, end='')
    # print("MAP")
    print("We found {} paths to get to the end.".format(len(results)))
    print("Shortest path was {} steps to reach the end".format(min_steps))