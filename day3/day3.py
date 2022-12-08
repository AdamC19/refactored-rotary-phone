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


if __name__ == "__main__":
    file_list = os.listdir()
    for i in range(0, len(file_list)):
        print("{}\t{}".format(i, file_list[i]))

    try:
        fname = file_list[int(input("Line Number: "))]
    except IndexError or ValueError:
        fname = "rucksacks.txt"

    f = open(fname, 'r')

    for line in f:
        all_items = line.strip()
        comp_1 = []
        comp_2 = []
        for i in range(0, len(all_items)):
            if i < len(all_items)/2:
                comp_1.append(all_items[i])
            else:
                comp_2.append(all_items[i])
        


    f.close()