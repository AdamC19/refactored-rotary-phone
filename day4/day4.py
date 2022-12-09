import os

#------------------------------------------------------------------------------
def is_fully_contained(rng_a, rng_b):
    # check if A fully contains B or if B fully contains A
    return (rng_a[0] <= rng_b[0] and rng_a[1] >= rng_b[1]) or (rng_b[0] <= rng_a[0] and rng_b[1] >= rng_a[1])
#------------------------------------------------------------------------------
def overlapping(rng_a, rng_b):
    return (rng_a[1] >= rng_b[0] and rng_a[0] <= rng_b[1] ) or (rng_a[0] <= rng_b[1] and rng_a[1] >= rng_b[0])
#------------------------------------------------------------------------------
   

file_list = os.listdir()
for i in range(0, len(file_list)):
    print("{}\t{}".format(i, file_list[i]))

try:
    fname = file_list[int(input("Line Number: "))]
except IndexError or ValueError:
    fname = "camp.txt"

f = open(fname, 'r')

n_fully_contains = 0
n_overlapping    = 0
for line in f:
    pairs_str = line.strip().split(',')
    pair_a_str = pairs_str[0].split('-')
    pair_b_str = pairs_str[1].split('-')

    pair_a = ( int(pair_a_str[0]), int(pair_a_str[1]) )
    pair_b = ( int(pair_b_str[0]), int(pair_b_str[1]) )

    if is_fully_contained(pair_a, pair_b):
        n_fully_contains += 1

    if overlapping(pair_a, pair_b):
        n_overlapping += 1

print("Assignment pairs where one range fully contains the other : {}".format(n_fully_contains))
print("Assignment pairs where one range overlaps the other at all: {}".format(n_overlapping))
