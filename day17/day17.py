import os
import copy

ROCK_SEQ = [ 
    [['@','@','@','@']], 
    [['.','@','.'], ['@','@','@'], ['.','@','.']], 
    [['@','@','@'], ['.','.','@'], ['.','.','@']],
    [['@'],['@'],['@'],['@']],
    [['@', '@'],['@','@']],
]
CAVE_WIDTH = 7
CAVE_START_H = 4

EMPTY_ROW = ['|','.','.','.','.','.','.','.','|']

CAVE_START = []
for row in range(0, CAVE_START_H):
    arr = ['|']
    for i in range(0, CAVE_WIDTH):
        arr.append('.')
    arr.append('|')
    CAVE_START.append(arr)

ROCK_APPEAR_AT_X    = 3
#-----------------------------------------------------------------------------
def print_cave(cave):
    for y in range(len(cave) - 1, -1, -1):
        for x in range(0, len(cave[y])):
            print(cave[y][x], end='')
        print('')
    print('+', end='')
    print('-'*(len(cave[0])-2), end='')
    print('+')

#-----------------------------------------------------------------------------
def find_falling_rock(cave):
    """ Find the index of the top of the falling rock"""
    y = len(cave) - 1
    # search for the begining of our falling rock
    while y >= 0 and '@' not in cave[y]:
        y -= 1
    
    return y
#-----------------------------------------------------------------------------
def add_rock(cave, rock):
    rock_h = len(rock)
    
    # search for topmost rock or floor
    top = len(cave) - 1
    while top >= 0 and '#' not in cave[top]:
        top -= 1

    y = top + 4 # extra plus one to account for the existing placed rock

    for rock_row in rock:
        x = ROCK_APPEAR_AT_X
        for rock_unit in rock_row:
            try:
                cave[y][x] = rock_unit
            except IndexError:
                cave.append(copy.deepcopy(EMPTY_ROW))
                cave[y][x] = rock_unit
            x += 1
        y += 1
#-----------------------------------------------------------------------------
def nudge_rock(cave, nudge):
    """  """
    
    y = len(cave) - 1
    # search for the begining of our falling rock
    while y >= 0 and '@' not in cave[y]:
        y -= 1
    
    if y < 0:
        return

    # check if we can nudge our rock over
    yy = y
    nudge_ok = True
    while nudge_ok and '@' in cave[yy]:
        if nudge == '>':
            last_unit = cave[yy][0]
            x = 0
            unit = cave[yy][x]
            found_edge = False
            while x < len(cave[yy]) and not found_edge:
                x += 1
                unit = cave[yy][x]
                if unit != '@' and last_unit == '@':
                    found_edge = True
                last_unit = unit
                

            nudge_ok = found_edge and cave[yy][x] == '.'

        elif nudge == '<':
            x = 0
            unit = cave[yy][x]
            next_unit = cave[yy][x+1]
            found_edge = False
            while x < len(cave[yy]) - 2 and not found_edge:
                x += 1
                unit = cave[yy][x]
                next_unit = cave[yy][x+1]
                if next_unit == '@' and unit != '@':
                    found_edge = True
            nudge_ok = found_edge and unit == '.'

        yy -= 1

    if nudge_ok:
        while '@' in cave[y]:
            if nudge == '>':
                # find index to remove space from
                x = 0
                found_edge = False
                while not found_edge:
                    x += 1
                    found_edge = cave[y][x] == '.' and cave[y][x-1] == '@'
                    
                pop_ind = x
                if cave[y][pop_ind] == '.':
                    # we can shift right
                    cave[y].pop(pop_ind)
                
                # now find insert index
                x = 0
                found_edge = False
                while not found_edge:
                    x += 1
                    found_edge = cave[y][x-1] != '@' and cave[y][x] == '@'
                cave[y].insert(x, '.')
                
            elif nudge == '<':
                # find index to remove space from
                x = 0
                found_edge = False
                while not found_edge:
                    x += 1
                    found_edge = cave[y][x] == '.' and cave[y][x+1] == '@'
                pop_ind = x
                if cave[y][pop_ind] == '.':
                    # we can shift everything left
                    cave[y].pop(pop_ind)
                
                # now find index to insert space at
                x = 1
                found_edge = False
                while not found_edge:
                    x += 1
                    found_edge = cave[y][x-1] == '@' and cave[y][x] != '@'
                cave[y].insert(x, '.')

            y -= 1

#-----------------------------------------------------------------------------
def shift_rock_down(cave):
    """ returns True if shift was completed, False if a downward move is not possible. """
    y = len(cave) - 1
    # search for the begining of our falling rock
    while y >= 0 and '@' not in cave[y]:
        y -= 1
    
    if y < 0:
        return False

    yy = y
    while yy >= 0 and '@' in cave[yy]:
        yy -= 1
    
    if yy < 0:
        return False

    rock_bottom = yy + 1
    rock_top = y
    y = rock_bottom
    move_ok = True
    # evaluate if move is possible
    while move_ok and y <= rock_top:
        for x in range(1, len(cave[y]) - 1):
            if cave[y][x] == '@':
                move_ok = move_ok and cave[y-1][x] != '#'
        y += 1
    if move_ok:
        y = rock_bottom
        while y <= rock_top:
            for x in range(1, len(cave[y]) - 1):
                if cave[y][x] == '@':
                    cave[y][x] = '.' # leave empty space
                    cave[y-1][x] = '@' # shift rock unit down
            y += 1

    return move_ok

#-----------------------------------------------------------------------------
def solidify_rock(cave):
    """ True if operation complete. False if no rock found. """
    y = find_falling_rock(cave)

    if y < 0:
        # no rock found
        return False
    
    while y >= 0 and '@' in cave[y]:
        for x in range(1, len(cave[y]) - 1):
            if cave[y][x] == '@':
                cave[y][x] = '#'
        y -= 1
    return True
#-----------------------------------------------------------------------------
def get_rock_height(cave):
    height = len(cave) - 1
    while height >= 0 and '#' not in cave[height]:
        height -= 1
    return height + 1
#-----------------------------------------------------------------------------
# def shift_tower_down(cave):

#-----------------------------------------------------------------------------
if __name__ == "__main__":
    file_list = os.listdir()
    for i in range(0, len(file_list)):
        print("{}\t{}".format(i, file_list[i]))

    try:
        fname = file_list[int(input("Line Number: "))]
    except IndexError or ValueError:
        fname = "input.txt"

    f = open(fname, 'r')

    jets = list(f.readline().strip())
    f.close()
    print(jets)

    cave = copy.deepcopy(CAVE_START)

    print_cave(cave)

    cave_start_y = 3

    rock_seq_ind = 0
    nudge_ind = 0

    stopped_rocks = 0

    stopped_count = int(input("Rock Count: "))
    height = 0
    while stopped_rocks < stopped_count:
        
        add_rock(cave, ROCK_SEQ[rock_seq_ind])
        stopped_rocks += 1
        # print_cave(cave)
        falling = True
        while falling:
            nudge_rock(cave, jets[nudge_ind])
            falling = shift_rock_down(cave)
            nudge_ind += 1
            if nudge_ind >= len(jets):
                nudge_ind = 0

        solidify_rock(cave)

        rock_seq_ind += 1
        if rock_seq_ind >= len(ROCK_SEQ):
            rock_seq_ind = 0
    
    print_cave(cave)
    print("==== RESULTS ====")
    height = get_rock_height(cave)
    print("Rock tower height after {} rocks: {}".format(stopped_rocks, height))
    print("=================")