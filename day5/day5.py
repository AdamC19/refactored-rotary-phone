import os
import copy

#------------------------------------------------------------------------------
def grab_topmost_crate(column, crates):
    row = 0
    col = column - 1
    while row < len(crates) and crates[row][col] == ' ':
        row += 1
    
    if row < len(crates):
        retval = crates[row][col] # grab value of the crate
        crates[row][col] = ' '    # replace crate with a space (no crate)
        return retval
    else:
        return  ' '
#------------------------------------------------------------------------------
def grab_topmost_chunk(num, column, crates):
    chunk = []
    row = 0
    col = column - 1
    while crates[row][col] == ' ' and row < len(crates):
        row += 1
    
    for i in range(0, num):
        chunk.append(crates[row + i][col]) # store value of this crate
        crates[row + i][col] = ' ' # replace crate with a space (no crate)

    return chunk
#------------------------------------------------------------------------------
def place_crate(column, crate, crates):
    row = 0
    col = column - 1
    while row < len(crates) and crates[row][col] == ' ':
        row += 1

    if row > 0:
        # place the crate on top.
        # row to actually place crate in is one up from where we saw the
        # first crate
        crates[row - 1][col] = crate 
    else:
        # insert a new empty row on top of the stack
        new_row = []
        for i in range(0, len(crates[0])):
            new_row.append(' ')
        crates.insert(0, new_row)
        crates[0][col] = crate # now place the crate on new 0th row
#------------------------------------------------------------------------------
def place_crate_chunk(column, chunk, crates):
    row = 0
    col = column - 1
    while row < len(crates) and crates[row][col] == ' ':
        row += 1

    row -= 1
    
    for i in range(len(chunk) - 1, -1, -1):
        # start from the bottom-most crate, place upwards
        crates[row][col] = chunk[i]
        row -= 1 # move upward
        if row < 0:
            # insert a new empty row on top of the stack
            new_row = []
            for i in range(0, len(crates[0])):
                new_row.append(' ')
            crates.insert(0, new_row)
            row = 0

#------------------------------------------------------------------------------
def process_move(num, start, dest, crates):
    for i in range(0, num):
        crate = grab_topmost_crate(start, crates)
        place_crate(dest, crate, crates)
#------------------------------------------------------------------------------
def scrape_top_of_stack(crates):
    retval = ''
    for col in range(0, len(crates[0])):
        row = 0
        while row < len(crates) and crates[row][col] == ' ':
            row += 1
        if row < len(crates):
            retval = retval + crates[row][col]
        else:
            retval = retval + ' '
    return retval
#------------------------------------------------------------------------------
def process_move_9001(num, start, dest, crates):
    # chunk = grab_topmost_chunk(num, start, crates)
    # place_crate_chunk(dest, chunk, crates)
    chunk = []
    for i in range(0, num):
        chunk.append(grab_topmost_crate(start, crates))
    for i in range(len(chunk) - 1, -1, -1):
        place_crate(dest, chunk[i], crates)
#------------------------------------------------------------------------------

file_list = os.listdir()
for i in range(0, len(file_list)):
    print("{}\t{}".format(i, file_list[i]))

try:
    fname = file_list[int(input("Line Number: "))]
except IndexError or ValueError:
    fname = "camp.txt"

f = open(fname, 'r')

mode = 0
crates = []
crates_9001 = None
stack_depth = 0
for line in f:

    if mode == 0:
        # we're reading in crate stack data
        if len(line) <= 1:
            # empty line indicates end of crate data
             # discard column numbering row from crate array
            crates.pop(len(crates)-1)
            crates_9001 = copy.copy(crates)
            print("="*79)
            print("CRATE ARRAY:")
            print("="*79)
            for row in crates:
                print(row)
            print("="*79)
           
            mode += 1 # goto movement mode
        else:
            # take bites of size 4
            last_i = 0
            crate_row = []
            for i in range(4, len(line) + 4, 4):
                crate = line[last_i : i - 1]
                if crate.isspace():
                    crate = ' '
                else:
                    crate = crate.strip('[]')
                crate_row.append(crate)
                last_i = i

            crates.append(crate_row)

        stack_depth += 1
    else:
        count   = 0
        start   = 0
        dest    = 0
        words = line.split(' ')
        for word in words:
            try:
                num = int(word)
                if count == 0:
                    count = num
                elif start == 0:
                    start = num
                elif dest == 0:
                    dest = num
                    break
            except ValueError:
                pass
        process_move(count, start, dest, crates)
        process_move_9001(count, start, dest, crates_9001)

print("="*79)
print("FINAL CRATE ARRAY:")
print("="*79)
for row in crates:
    print(row)
print("="*79)
print("\nTop-most crates are: {}".format(scrape_top_of_stack(crates)))

print("="*79)
print("FINAL CRATE ARRAY 9001:")
print("="*79)
for row in crates_9001:
    print(row)
print("="*79)
print("\nTop-most crates are: {}".format(scrape_top_of_stack(crates_9001)))
f.close()

f = open(fname, 'r')

