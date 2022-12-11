import os


#------------------------------------------------------------------------------
file_list = os.listdir()
for i in range(0, len(file_list)):
    print("{}\t{}".format(i, file_list[i]))

try:
    fname = file_list[int(input("Line Number: "))]
except IndexError or ValueError:
    fname = "instructions.txt"

f = open(fname, 'r')

cycles_to_check = [20, 60, 100, 140, 180, 220]
ans = 0

cycle_ctr = 1
x = 1
crt_pos = 0
crt_lines = []
for i in range(0, 6):
    for ii in range(0, 40):
        crt_lines.append('.')

for line in f:
    inst = line.strip()
    
    if "noop" in inst:
        if cycle_ctr in cycles_to_check:
            sig_strength = cycle_ctr * x
            ans += sig_strength
            # print("During cycle {} we have signal strength of {}".format(cycle_ctr, sig_strength))
        cycle_ctr += 1
        # check if our sprite is in the right spot to be displayed
        for i in range(-1, 2, 1):
            if crt_pos % 40 == (x + i):
                crt_lines[crt_pos] = '#'
        crt_pos += 1
    elif "addx" in inst:
        for i in range(0, 2):
            if cycle_ctr in cycles_to_check:
                sig_strength = cycle_ctr * x
                ans += sig_strength
                # print("During cycle {} we have signal strength of {}".format(cycle_ctr, sig_strength))
            cycle_ctr += 1
            
            # check if our sprite is in the right spot to be displayed
            for i in range(-1, 2, 1):
                if crt_pos % 40 == (x + i):
                    crt_lines[crt_pos] = '#'
            crt_pos += 1

        num = int(inst.split(' ')[1])
        x += num

crt_line = ''
print("====== DISPLAY OUTPUT ======")
for i in range(0, len(crt_lines)):
    if i % 40 == 0 or i == len(crt_lines) - 1:
        print(crt_line)
        crt_line = ''
    crt_line += crt_lines[i]
print("============================")

print("Answer is : {}".format(ans))
f.close()
