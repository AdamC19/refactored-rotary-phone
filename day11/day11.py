import os
import copy
prime_fact_dict = {
    2: 0,
    3: 0,
    5: 0,
    7: 0,
    11: 0,
    13: 0,
    17: 0,
    19: 0,
    23: 0,
    29: 0,
    31: 0,
    37: 0,
    41: 0,
    43: 0,
    47: 0,
    53: 0,
    59: 0,
    61: 0,
    67: 0,
    71: 0,
    73: 0,
    79: 0,
    83: 0,
    89: 0,
    97: 0
}
#------------------------------------------------------------------------------
def is_prime(num):
    if num > 1:
        for i in range(2, (num >> 1) + 1):
            if (num % i) == 0:
                return False
        return True
    else:
        return False
#------------------------------------------------------------------------------
def prime_factorization(num): #, factors):
    factors = copy.copy(prime_fact_dict)
    if is_prime(num):
        factors[num] = 1
    else:
        for key in factors.keys():
            while num % key == 0:
                factors[key] += 1
                num = num / key
        if is_prime(num):
            try:
                factors[int(num)] += 1
            except KeyError:
                factors[int(num)] = 1
            
    return factors
#------------------------------------------------------------------------------
def number_from_factors(factors):
    retval = 1
    for key in factors.keys():
        retval *= key ** factors[key]
    return retval
#------------------------------------------------------------------------------
class Monkey(object):
    def __init__(self, id):
        self.id = id
        self.item_worry_list = []
        self.worry_func = None
        self.test = 1
        self.if_true = 0
        self.if_false = 0
        self.operator = ''
        self.operand = 0
        self.inspections = 0

    def inspect_item(self):
        item = self.item_worry_list.pop(0)
        self.inspections += 1
        if self.operator == '+':
            # new_num = number_from_factors(item)
            # new_num += self.operand
            # factors = prime_factorization(new_num) #copy.copy(prime_fact_dict)
            # prime_factorization(new_num, factors)
            return item + self.operand #factors
        elif self.operator == '*':
            if type(self.operand) == type(None):
                # if is_prime(item):
                # item = item**2
                pass
                # for key in item.keys():
                #     if item[key] > 0:
                #         item[key] += 1
            else:
                # item[self.operand] += 1
                if item % self.operand != 0:
                    # item is not already divisible by this operand
                    item *= self.operand
            return item
#------------------------------------------------------------------------------
def print_monke(monke):
    print("Monkey {}:".format(monke.id))
    print("  Starting items: {}".format(monke.item_worry_list))
    print("  Test: divisible by {}".format(monke.test))
    print("    If true: throw to monkey {}".format(monke.if_true))
    print("    If false: throw to monkey {}".format(monke.if_false))
#------------------------------------------------------------------------------
def print_round(monkeys):
    for monk in monkeys:
        print("Monkey {}: {}".format(monk.id, monk.inspections))
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

    monkeys = []
    current_monkey = 0
    divide_by = 1

    for line in f:
        parts = line.strip().split(':')
        if "Monkey" in parts[0]:
            id = int(parts[0].split(' ')[1])
            monkeys.append(Monkey(id))
            current_monkey = id
        elif "Starting items" in parts[0]:
            item_strs = parts[1].split(',')
            for s in item_strs:
                num = int(s)
                # factors = prime_factorization(num) #copy.copy(prime_fact_dict)
                monkeys[current_monkey].item_worry_list.append(num) #factors)
        elif "Operation" in parts[0]:
            if '+' in parts[1]:
                num = int(parts[1].split('+')[1])
                monkeys[current_monkey].operator = '+'
                monkeys[current_monkey].operand = num
                # monkeys[current_monkey].worry_func = lambda old : old + num
            elif '*':
                monkeys[current_monkey].operator = '*'
                try:
                    num = int(parts[1].split('*')[1])
                    monkeys[current_monkey].operand = num
                    # monkeys[current_monkey].worry_func = lambda old : old * num
                except ValueError:
                    # monkeys[current_monkey].worry_func = lambda old : old * old
                    monkeys[current_monkey].operand = None

        elif "Test" in parts[0]:
            div_by = int(parts[1].strip().split(' ')[2])
            monkeys[current_monkey].test = div_by
        elif "If true" in parts[0]:
            monkeys[current_monkey].if_true = int(parts[1].strip().split(' ')[3])
        elif "If false" in parts[0]:
            monkeys[current_monkey].if_false = int(parts[1].strip().split(' ')[3])

    for monk in monkeys:
        print_monke(monk)

    N_ROUNDS = 10000

    for i in range(1, N_ROUNDS + 1):
        for monk in monkeys:
            while len(monk.item_worry_list) > 0:
                # item = monk.item_worry_list.pop(0)      # monkey inspects item
                worry_level = monk.inspect_item() #monk.worry_func(item)
                # worry_level = int(worry_level/3)    # monkey gets bored, worry divides
                # run divisiblity test, choosing monkey to throw to
                throw_to = monk.if_false
                if worry_level % monk.test == 0:
                # if worry_level[monk.test] > 0:
                    throw_to = monk.if_true
                
                # throw to monkey
                monkeys[throw_to].item_worry_list.append(worry_level)
        if (i) % 1000 == 0:
            print("After round {}...".format(i))
            print_round(monkeys)     
            print("") 
        # input("Continue? [ENTER]")       

    most_active = []
    for monk in monkeys:
        print("Monkey {}: {} inspections".format(monk.id, monk.inspections))
        most_active.append(monk.inspections)

    highest = max(most_active)
    for i in range(0, len(most_active)):
        if most_active[i] == highest:
            most_active.pop(i)
            break

    next_highest = max(most_active)
    print("LEVEL OF MONKEY BUSINESS = {}".format(highest*next_highest))