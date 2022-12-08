import os

file_list = os.listdir()
for i in range(0, len(file_list)):
    print("{}\t{}".format(i, file_list[i]))

try:
    fname = file_list[int(input("Line Number: "))]
except IndexError or ValueError:
    fname = "calories.txt"

f = open(fname, 'r')

calories = 0
max_calories = 0
for line in f:
    if line == '\n':
        if calories > max_calories:
            max_calories = calories
        calories = 0
    else:
        calories += int(line.strip())

f.close()

print("Some very prepared elf is carrying {} calories!".format(max_calories))

f = open(fname, 'r')

top_three = [0,0,0]
calories = 0
for line in f:
    if line == '\n':
        # starting at the lowest index,
        # see if calories is greater than the value at that index
        i = 0
        # print("Calories = {}".format(calories))
        while i < 3 and calories > top_three[i]:
            i += 1

        if i <= 3 and i > 0:
            top_three.insert(i, calories)
            top_three.pop(0)

        calories = 0
    else:
        calories += int(line.strip())

sum_3 = 0
for val in top_three:
    sum_3 += val

print("The top 3 most prepared elves are carrying {} calories - a total of {} calories!".format(top_three, sum_3))
f.close()