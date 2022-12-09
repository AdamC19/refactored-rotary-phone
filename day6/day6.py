import os


file_list = os.listdir()
for i in range(0, len(file_list)):
    print("{}\t{}".format(i, file_list[i]))

try:
    fname = file_list[int(input("Line Number: "))]
except IndexError or ValueError:
    fname = "datastream.txt"

f = open(fname, 'r')

line = f.readline()

start = 0
end = 0

window = []
found_marker = False
while not found_marker and end < len(line):
    end = start + 4
    window = list(line[start : end])

    marker = True
    for i in range(0, 4):
        letter = window.pop(0)
        if letter in window:
            marker = False
            break
    
    found_marker = marker

    start += 1

print("Found marker after {} characters.".format(end))

start = 0
end = 0

window = []
found_marker = False
while not found_marker and end < len(line):
    end = start + 14
    window = list(line[start : end])

    marker = True
    for i in range(0, 14):
        letter = window.pop(0)
        if letter in window:
            marker = False
            break
    
    found_marker = marker

    start += 1

print("Found start-of-message marker after {} characters.".format(end))
