import os
import copy


#------------------------------------------------------------------------------
def is_tail_near_head(head_pos, tail_pos):
    retval = False
    if abs(head_pos[0] - tail_pos[0]) <= 1:
        # within striking distance in the X axis
        if abs(head_pos[1] - tail_pos[1]) <= 1:
            # within striking distance in Y axis too
            retval = True
        # else, out of range in Y -> leave retval false

    # else, out of range in X axis -> leave reval false

    return retval
#------------------------------------------------------------------------------
def sign(num):
    if num < 0:
        return -1
    elif num > 0:
        return 1
    else:
        return 0
#------------------------------------------------------------------------------
def move_head_drag_tail(head_pos, tail_pos):
    new_tail_pos = [tail_pos[0], tail_pos[1]]
    if not is_tail_near_head(head_pos, tail_pos):
        x_delta = head_pos[0] - tail_pos[0]
        y_delta = head_pos[1] - tail_pos[1]
        if abs(x_delta) > 1:
            if x_delta > 1:
                new_tail_pos[0] = new_tail_pos[0] + (x_delta - 1)
                if abs(y_delta) >= 1:
                    # this is a case where tail was diagonal from head
                    # in this case, resolve the y_delta
                    new_tail_pos[1] = new_tail_pos[1] + sign(y_delta) # y_delta

            elif x_delta < -1:
                new_tail_pos[0] = new_tail_pos[0] + (x_delta + 1)
                if abs(y_delta) >= 1:
                    # this is a case where tail was diagonal from head
                    # in this case, resolve the y_delta
                    new_tail_pos[1] = new_tail_pos[1] + sign(y_delta) # y_delta
        elif abs(y_delta) > 1:
            if y_delta > 1:
                new_tail_pos[1] = new_tail_pos[1] + (y_delta - 1)
                if abs(x_delta) >= 1:
                    # this is a case where tail was diagonal from head
                    # in this case, resolve the y_delta
                    new_tail_pos[0] = new_tail_pos[0] + sign(x_delta) # x_delta
            elif y_delta < -1:
                new_tail_pos[1] = new_tail_pos[1] + (y_delta + 1)
                if abs(x_delta) >= 1:
                    # this is a case where tail was diagonal from head
                    # in this case, resolve the y_delta
                    new_tail_pos[0] = new_tail_pos[0] + sign(x_delta) # x_delta
                    
    return new_tail_pos
#------------------------------------------------------------------------------
def print_rope_space(space):
    for y in range(len(space[0]) - 1, -1, -1):
        for x in range(0, len(space)):
            print(space[x][y], end='')
        print("")
#------------------------------------------------------------------------------
file_list = os.listdir()
for i in range(0, len(file_list)):
    print("{}\t{}".format(i, file_list[i]))

try:
    fname = file_list[int(input("Line Number: "))]
except IndexError or ValueError:
    fname = "rope.txt"

f = open(fname, 'r')

space = [['H']] # start with only the start position
space_tail = [['#']] # for tracking where the tail has been
head_pos = [0, 0]
tail_pos = [0, 0]
for line in f:
    parts = line.strip().split(' ')
    direc = parts[0]
    steps = int(parts[1])
    sign_x = 0
    sign_y = 0
    if direc == 'U':
        sign_y = 1
    elif direc == 'R':
        sign_x = 1
    elif direc == 'D':
        sign_y = -1
    elif direc == 'L':
        sign_x = -1

    for i in range(0, steps):
        # move one step in designated direction
        # just computing new head coordinates
        new_head_pos = [head_pos[0] + sign_x, head_pos[1] + sign_y]
        
        try:
            if new_head_pos[0] < 0:
                # add a new column TO THE LEFT
                new_col = []
                for i in space[0]:
                    new_col.append('.')
                space.insert(0, new_col)
                space_tail.insert(0, copy.copy(new_col))
                new_head_pos[0] = 0
                # MUST INCREMENT TAIL POSITION BECAUSE WE GREW TO THE LEFT
                tail_pos[0] += 1
            elif new_head_pos[1] < 0:
                # add a new row to each column AT THE BOTTOM
                for i in range(0, len(space)):
                    space[i].insert(0, '.')
                    space_tail[i].insert(0, '.')
                new_head_pos[1] = 0
                # MUST INCREMENT TAIL POSITION BECAUSE WE GREW DOWNWARDS
                tail_pos[1] += 1

            space[head_pos[0]][head_pos[1]] = '.'
            space[new_head_pos[0]][new_head_pos[1]] = 'H'
        except IndexError:
            # print("Growing to the {}".format(direc))
            if new_head_pos[0] >= len(space):
                # add a new column
                new_col = []
                for i in space[0]:
                    new_col.append('.')
                space.append(new_col)
                space_tail.append(copy.copy(new_col))

            elif new_head_pos[1] >= len(space[0]):
                # add a new row to each column
                for i in range(0, len(space)):
                    space[i].append('.')
                    space_tail[i].append('.')
            
            space[new_head_pos[0]][new_head_pos[1]] = 'H'

        new_tail_pos = move_head_drag_tail(new_head_pos, tail_pos)
        if new_tail_pos != tail_pos:
            # if tail has been dragged, replace tail with # and move tail
            space_tail[tail_pos[0]][tail_pos[1]] = '#'
            space_tail[new_tail_pos[0]][new_tail_pos[1]] = '#' # ensure this is captured also
            space[new_tail_pos[0]][new_tail_pos[1]] = 'T'
            tail_pos = new_tail_pos

        # last step
        head_pos = new_head_pos
f.close()

print_rope_space(space_tail)

total = 0
for col in space_tail:
    for spot in col:
        if spot == '#':
            total += 1
print(len(space_tail))
print("The tail saw {} spots as it was dragged around.".format(total))

########
# PART 2
########

f = open(fname, 'r')

space = [['H']] # start with only the start position
space_tail = [['#']] # for tracking where the tail has been

rope = []
ROPE_LEN = 10
for i in range(0, ROPE_LEN):
    rope.append([0,0])

for line in f:
    parts = line.strip().split(' ')
    direc = parts[0]
    steps = int(parts[1])
    sign_x = 0
    sign_y = 0
    if direc == 'U':
        sign_y = 1
    elif direc == 'R':
        sign_x = 1
    elif direc == 'D':
        sign_y = -1
    elif direc == 'L':
        sign_x = -1

    for not_used in range(0, steps):
        # first, compute a new head position
        new_head_pos = [rope[0][0] + sign_x, rope[0][1] + sign_y]
        
        if new_head_pos[0] < 0:
            # add a new column TO THE LEFT
            new_col = []
            for i in space_tail[0]:
                new_col.append('.')
            # space.insert(0, new_col)
            space_tail.insert(0, new_col) #copy.copy(new_col))
            new_head_pos[0] = 0
            # MUST INCREMENT ALL OTHER POSITIONS BECAUSE WE GREW TO THE LEFT
            # tail_pos[0] += 1
            for i in range(1, ROPE_LEN):
                rope[i][0] = rope[i][0] + 1
        elif new_head_pos[1] < 0:
            # add a new row to each column AT THE BOTTOM
            for i in range(0, len(space_tail)):
                # space[i].insert(0, '.')
                space_tail[i].insert(0, '.')
            new_head_pos[1] = 0
            # MUST INCREMENT ALL OTHER POSITIONS BECAUSE WE GREW DOWNWARDS
            # tail_pos[1] += 1
            for i in range(1, ROPE_LEN):
                rope[i][1] = rope[i][1] + 1
        elif new_head_pos[0] >= len(space_tail):
            # add a new column
            new_col = []
            for i in space_tail[0]:
                new_col.append('.')
            space.append(new_col)
            space_tail.append(new_col)

        elif new_head_pos[1] >= len(space_tail[0]):
            # add a new row to each column
            for i in range(0, len(space_tail)):
                # space[i].append('.')
                space_tail[i].append('.')

        rope[0] = new_head_pos

        for i in range(1, ROPE_LEN):
            new_knot_pos = move_head_drag_tail(rope[i-1], rope[i])
            if new_knot_pos != rope[i]:
                rope[i] = new_knot_pos
            else:
                break
            # if i == 9:
            #     # this is the tail
        space_tail[rope[9][0]][rope[9][1]] = '#'

f.close() 

# print_rope_space(space_tail)

total = 0
for col in space_tail:
    for spot in col:
        if spot == '#':
            total += 1

print(len(space_tail))
print("The tail saw {} spots as it was dragged around.".format(total))