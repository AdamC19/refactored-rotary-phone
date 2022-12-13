import os
import copy

#------------------------------------------------------------------------------
def listify(s, depth):
    s = s[1:] # omit the start cap
    # if len(s) > 0 and s[len(s) - 1] == ']':
    #     # print("chop end cap off")
    #     s = s[: len(s) - 1]
    #     print('string is now "{}"'.format(s))

    retval = []
    end = 0
    i = 0
    while len(s) > 0 and i < len(s): # in range(0, len(s)):
        if s[i] == '[':
            end = i
            while end < len(s) - 1 and s[end] != ']':
                # print("string = {}".format(s))
                end += 1
            # start of a new list
            # print("Start of a new list (depth = {})".format(depth + 1))
            retval.append(listify(s[i:end], depth + 1))
            i = end + 1
        elif s[i] == ']':
            # end of whatever list we're on
            # print("End of current list level (depth = {})".format(depth))
            pass
        else:
            try:
                num = int(s[i])
                # print("Appending {} to retval".format(num))
                retval.append(num)
                # print("Appended.")
            except ValueError:
                pass
        
        i += 1
        # print("i = {}".format(i))
    # print(retval)
    return retval

#------------------------------------------------------------------------------
def compare_lists(left, right):
    """ returns 1 if left comes before right (correct order), 
    -1 if right before left (wrong order), or 0 if we need to continue
     """
    print("COMPARING: {} vs {}".format(left, right), end='\t')
    result = 0
    end_of_list = False
    i = 0
    while result == 0 and not end_of_list: # and not end_of_list:
        try:
            if type(left[i]) is int and type(right[i]) is int:
                if left[i] < right[i]:
                    result = 1
                elif left[i] > right[i]:
                    result = -1
                else:
                    pass
                    # proceed to next element
                    # print("Next element")
                    # i += 1
            elif type(left[i]) is list and type(right[i]) is list:
                result = compare_lists(left[i], right[i])
            elif type(left[i]) is list:
                result = compare_lists(left[i], [right[i]])
            elif type(right[i]) is list:
                result = compare_lists([left[i]], right[i])

        except IndexError:
            # we haven't found a valid comparison
            # either we've run out of elements, or lists are lengthed differently
            if len(left) < len(right):
                result = 1
            elif len(left) > len(right):
                result = -1
            else:
                # print("End of a list")
                result = 0
                end_of_list = True
        i += 1
    print("RESULT = {}".format(result))
    return result

#------------------------------------------------------------------------------



if __name__ == "__main__":
    file_list = os.listdir()
    for i in range(0, len(file_list)):
        print("{}\t{}".format(i, file_list[i]))

    try:
        fname = file_list[int(input("Line Number: "))]
    except IndexError or ValueError:
        fname = "distress.txt"

    f = open(fname, 'r')

    pair_ind = 1
    ind = 'left'
    pairs = {}
    pair = {}
    for line in f:
        if len(line.strip()) < 1:
            # print("PAIR of INDEX {}".format(pair_ind))
            # print(pair[0])
            # print(pair[1])
            # print("")
            pairs[pair_ind] = copy.deepcopy(pair)
            pair_ind += 1
            ind = 'left'
        else:
            # LIST-IFY
            pair[ind] = listify(line.strip(), 0)
            ind = 'right'

    f.close()

    sum_of_indices = 0
    for i in pairs.keys():
        print(" PAIR {}: \t".format(i), end='')
        # print("LEFT : ", end='')
        # print(pairs[i]['left'], end='\t')
        # print("RIGHT: ", end='')
        # print(pairs[i]['right'])
        
        result = compare_lists(pairs[i]['left'], pairs[i]['right'])
        if result == 1:
            print("CORRECT order")
            sum_of_indices += i
        elif result == -1:
            print("INCORRECT order")
        else:
            print("WTF")

        print("")
    
    print("===== RESULTS =====")
    print("Sum of correct indices: {}".format(sum_of_indices))
    print("===================")