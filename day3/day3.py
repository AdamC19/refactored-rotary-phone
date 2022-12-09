import os

#------------------------------------------------------------------------------
def decode_priority(letter):
    
    ascii_val = ord(letter)
    if ascii_val >= 65 and ascii_val <= 90:
        # upper case letters
        ind = (ord(letter) - 65) + 26
    elif ascii_val >= 97 and ascii_val <= 122:
        # lower case letters
        ind = (ord(letter) - 97)

    return ind + 1
#------------------------------------------------------------------------------
def find_common_letters(a, b):
    common = []
    for letter in a:
        if letter in b:
            common.append(letter)
    return common
#------------------------------------------------------------------------------

if __name__ == "__main__":
    file_list = os.listdir()
    for i in range(0, len(file_list)):
        print("{}\t{}".format(i, file_list[i]))

    try:
        fname = file_list[int(input("Line Number: "))]
    except IndexError or ValueError:
        fname = "rucksacks.txt"

    f = open(fname, 'r')

    priority_sum = 0

    for line in f:
        all_items = line.strip()
        halfway = int(len(all_items)/2)
        comp_1 = all_items[0:halfway]
        comp_2 = all_items[halfway:len(all_items)]
        
        common_letter = ''
        for letter in comp_1:
            if letter in comp_2:
                common_letter = letter
                break
        priority_sum += decode_priority(common_letter)
        
    print("Priority-Sum: {}".format(priority_sum))
    f.close()

    
    f = open(fname, 'r')

    line_counter = 0
    priority_sum = 0
    group = []
    for line in f:
        all_items = line.strip()
        group.append(all_items)
        line_counter += 1
        if line_counter % 3 == 0:
            # analyze this group of elves
            badge = ''
            for letter in group[0]:
                if letter in group[1] and letter in group[2]:
                    badge = letter
            priority_sum += decode_priority(badge)
            group = []
    
    print("Priority-Sum for badges: {}".format(priority_sum))

    f.close()